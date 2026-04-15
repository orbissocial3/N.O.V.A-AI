# backend/app/routes/plans.py
"""
Rutas de Planes Premium
-----------------------
Gestión de planes de suscripción en N.O.V.A.
Incluye validación avanzada, auditoría, métricas, trazabilidad y seguridad.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import List
from slowapi.util import get_remote_address

from app.db.postgresql import get_db
from app.models.plan import Plan
from app.utils.logger import get_logger
from app.utils.security import get_current_user
from app.monitoring import metrics, tracing, alerts

import time

logger = get_logger("plans")

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={404: {"description": "No encontrado"}}
)

# --- Modelos Pydantic para validación ---
class PlanCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    type: str = Field(..., pattern="^(basic|premium|enterprise)$")  # ✅ corregido
    price: float = Field(..., gt=0)
    duration_days: int = Field(..., gt=0, le=365)
    max_agents: int = Field(default=3, ge=1, le=50)
    max_storage_mb: int = Field(default=100, ge=10, le=100000)

    @validator("name")
    def validate_name(cls, v):
        if not v.replace("_", "").replace(" ", "").isalnum():
            raise ValueError("El nombre del plan debe ser alfanumérico (se permiten espacios y guiones bajos)")
        return v.strip()

class PlanResponse(BaseModel):
    id: int
    name: str
    type: str
    price: float
    duration_days: int
    max_agents: int
    max_storage_mb: int
    is_active: bool

    class Config:
        orm_mode = True

# --- Endpoints ---
@router.get("/", response_model=List[PlanResponse])
def list_plans(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    start = time.time()
    ip = get_remote_address(request)
    try:
        with tracing.start_span("plans:list"):
            plans = db.query(Plan).filter(Plan.is_active == True).all()
            logger.info(f"[PLANS] Listado solicitado | total={len(plans)} user={current_user.email} ip={ip}")
            metrics.record_request("GET", "/plans/")
            metrics.record_latency("/plans/", time.time() - start)
            return plans
    except Exception as e:
        metrics.record_error("/plans/", severity="CRITICAL")
        alerts.send_alert(f"Error al listar planes: {e}", severity="CRITICAL")
        logger.error(f"[PLANS] Error al listar planes: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al listar planes")

@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(request: PlanCreateRequest, req: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    start = time.time()
    ip = get_remote_address(req)
    try:
        with tracing.start_span("plans:create"):
            existing = db.query(Plan).filter(Plan.name == request.name).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un plan con ese nombre")

            plan = Plan(**request.dict())
            db.add(plan)
            db.flush()
            db.refresh(plan)
            db.commit()

            logger.info(f"[PLANS] Plan creado | id={plan.id} name={plan.name} by={current_user.email} ip={ip}")
            metrics.record_request("POST", "/plans/")
            metrics.record_latency("/plans/", time.time() - start)
            return plan
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        metrics.record_error("/plans/", severity="CRITICAL")
        alerts.send_alert(f"Error al crear plan: {e}", severity="CRITICAL")
        logger.error(f"[PLANS] Error al crear plan: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al crear plan")

@router.delete("/{plan_id}", status_code=status.HTTP_200_OK)
def delete_plan(plan_id: int, req: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    start = time.time()
    ip = get_remote_address(req)
    try:
        with tracing.start_span("plans:delete"):
            plan = db.query(Plan).filter(Plan.id == plan_id).first()
            if not plan:
                raise HTTPException(status_code=404, detail="Plan no encontrado")

            db.delete(plan)
            db.commit()
            logger.warning(f"[PLANS] Plan eliminado | id={plan_id} by={current_user.email} ip={ip}")
            metrics.record_request("DELETE", "/plans/{plan_id}")
            metrics.record_latency("/plans/{plan_id}", time.time() - start)
            return {"message": "Plan eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        metrics.record_error("/plans/{plan_id}", severity="CRITICAL")
        alerts.send_alert(f"Error al eliminar plan {plan_id}: {e}", severity="CRITICAL")
        logger.error(f"[PLANS] Error al eliminar plan {plan_id}: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar plan")
