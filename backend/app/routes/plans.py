# backend/app/routes/plans.py
"""
Rutas de Planes
---------------
Gestión de planes de suscripción en N.O.V.A.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.postgresql import get_db
from app.models.plan import Plan
from app.utils.logger import get_logger

logger = get_logger("plans")

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/")
def list_plans(db: Session = Depends(get_db)):
    """
    Lista todos los planes activos.
    """
    try:
        plans = db.query(Plan).filter(Plan.is_active == True).all()
        logger.info(f"[PLANS] Listado de planes solicitado | total={len(plans)}")
        return [plan.to_dict() for plan in plans]
    except Exception as e:
        logger.error(f"[PLANS] Error al listar planes: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar planes")

@router.post("/")
def create_plan(
    name: str,
    type: str,
    price: float,
    duration_days: int,
    max_agents: int = 3,
    max_storage_mb: int = 100,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo plan de suscripción.
    """
    try:
        # Validar duplicados
        existing = db.query(Plan).filter(Plan.name == name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un plan con ese nombre"
            )

        plan = Plan(
            name=name,
            type=type,
            price=price,
            duration_days=duration_days,
            max_agents=max_agents,
            max_storage_mb=max_storage_mb
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)

        logger.info(f"[PLANS] Plan creado | id={plan.id} name={plan.name}")
        return {"message": "Plan creado correctamente", "plan": plan.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[PLANS] Error al crear plan: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear plan")

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Elimina un plan por ID.
    """
    try:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")

        db.delete(plan)
        db.commit()
        logger.warning(f"[PLANS] Plan eliminado | id={plan_id}")
        return {"message": "Plan eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[PLANS] Error al eliminar plan {plan_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar plan")
