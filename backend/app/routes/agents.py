# backend/app/routes/agents.py
"""
Rutas de Agentes IA Premium
---------------------------
Gestión de agentes disponibles en N.O.V.A.
Incluye validación avanzada, auditoría, métricas, trazabilidad y seguridad.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import List
from app.db.postgresql import get_db
from app.models.agent import Agent
from app.utils.logger import get_logger
from app.utils.security import get_current_user
from app.monitoring import metrics, tracing, alerts
from slowapi.util import get_remote_address

import time

logger = get_logger("agents")

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "No encontrado"}}
)

# --- Modelos Pydantic ---
class AgentCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=255)
    category: str = Field(..., pattern="^(estudiante|programador|secretario|inversor|creativo)$")  # ✅ corregido
    is_premium: bool = False

    @validator("name")
    def validate_name(cls, v):
        if not v.replace("_", "").isalnum():
            raise ValueError("El nombre del agente debe ser alfanumérico (se permiten guiones bajos)")
        return v.strip()

class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    is_premium: bool
    is_active: bool

    class Config:
        orm_mode = True

# --- Endpoints ---
@router.get("/", response_model=List[AgentResponse])
def list_agents(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    start = time.time()
    ip = get_remote_address(request)
    try:
        with tracing.start_span("agents:list"):
            agents = db.query(Agent).filter(Agent.is_active == True).all()
            logger.info(f"[AGENTS] Listado solicitado | total={len(agents)} user={current_user.email} ip={ip}")
            metrics.record_request("GET", "/agents/")
            metrics.record_latency("/agents/", time.time() - start)
            return agents
    except Exception as e:
        metrics.record_error("/agents/", severity="CRITICAL")
        alerts.send_alert(f"Error al listar agentes: {e}", severity="CRITICAL")
        logger.error(f"[AGENTS] Error al listar agentes: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al listar agentes")

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(request: AgentCreateRequest, req: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    start = time.time()
    ip = get_remote_address(req)
    try:
        with tracing.start_span("agents:create"):
            existing = db.query(Agent).filter(Agent.name == request.name).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un agente con ese nombre")

            agent = Agent(**request.dict())
            db.add(agent)
            db.flush()
            db.refresh(agent)
            db.commit()

            logger.info(f"[AGENTS] Agente creado | id={agent.id} name={agent.name} by={current_user.email} ip={ip}")
            metrics.record_request("POST", "/agents/")
            metrics.record_latency("/agents/", time.time() - start)
            return agent
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        metrics.record_error("/agents/", severity="CRITICAL")
        alerts.send_alert(f"Error al crear agente: {e}", severity="CRITICAL")
        logger.error(f"[AGENTS] Error al crear agente: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al crear agente")

@router.delete("/{agent_id}", status_code=status.HTTP_200_OK)
def delete_agent(agent_id: int, req: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    start = time.time()
    ip = get_remote_address(req)
    try:
        with tracing.start_span("agents:delete"):
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise HTTPException(status_code=404, detail="Agente no encontrado")

            db.delete(agent)
            db.commit()
            logger.warning(f"[AGENTS] Agente eliminado | id={agent_id} by={current_user.email} ip={ip}")
            metrics.record_request("DELETE", "/agents/{agent_id}")
            metrics.record_latency("/agents/{agent_id}", time.time() - start)
            return {"message": "Agente eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        metrics.record_error("/agents/{agent_id}", severity="CRITICAL")
        alerts.send_alert(f"Error al eliminar agente {agent_id}: {e}", severity="CRITICAL")
        logger.error(f"[AGENTS] Error al eliminar agente {agent_id}: {e} | ip={ip}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar agente")
