# backend/app/routes/agents.py
"""
Rutas de Agentes IA
-------------------
Gestión de agentes disponibles en N.O.V.A.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.postgresql import get_db
from app.models.agent import Agent
from app.utils.logger import get_logger

logger = get_logger("agents")

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/")
def list_agents(db: Session = Depends(get_db)):
    """
    Lista todos los agentes disponibles.
    """
    try:
        agents = db.query(Agent).filter(Agent.is_active == True).all()
        logger.info(f"[AGENTS] Listado de agentes solicitado | total={len(agents)}")
        return [agent.to_dict() for agent in agents]
    except Exception as e:
        logger.error(f"[AGENTS] Error al listar agentes: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar agentes")

@router.post("/")
def create_agent(
    name: str,
    description: str,
    category: str,
    is_premium: bool = False,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo agente IA.
    """
    try:
        # Validar duplicados
        existing = db.query(Agent).filter(Agent.name == name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un agente con ese nombre"
            )

        agent = Agent(
            name=name,
            description=description,
            category=category,
            is_premium=is_premium
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        logger.info(f"[AGENTS] Agente creado | id={agent.id} name={agent.name}")
        return {"message": "Agente creado correctamente", "agent": agent.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AGENTS] Error al crear agente: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear agente")

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Elimina un agente por ID.
    """
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agente no encontrado")

        db.delete(agent)
        db.commit()
        logger.warning(f"[AGENTS] Agente eliminado | id={agent_id}")
        return {"message": "Agente eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AGENTS] Error al eliminar agente {agent_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar agente")
