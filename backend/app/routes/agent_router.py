"""
agent_router.py
-----------------------------------
Router maestro de agentes IA en N.O.V.A
- Direcciona mensajes al agente correcto
- Garantiza aislamiento entre agentes
- Controla acceso según plan (free/premium)
- Logging empresarial para trazabilidad
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi.util import get_remote_address

from app.db.postgresql import get_db
from app.utils.logger import get_logger
from app.models.user import User
from app.routes.auth_full import get_current_user

# Importar agentes
from app.services.agents.student import student_agent
from app.services.agents.investor_premium import investor_agent
from app.services.agents.secretary import secretary_agent
from app.services.agents.programmer import programmer_agent
from app.services.agents.creative_premium import creative_agent

logger = get_logger("agent_router")

router = APIRouter(
    prefix="/ask",
    tags=["agent_router"],
    responses={404: {"description": "Agente no encontrado"}}
)

# Mapeo de agentes disponibles
AGENTS = {
    "student": student_agent,
    "investor": investor_agent,
    "secretary": secretary_agent,
    "programmer": programmer_agent,
    "creative": creative_agent,
}

# Control de acceso por plan
PREMIUM_AGENTS = {"investor", "secretary", "programmer", "creative"}
FREE_AGENTS = {"student"}

@router.post("/")
def route_message(
    agent: str,
    message: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Direcciona el mensaje al agente correcto.
    - Valida existencia del agente
    - Aplica control de plan (free/premium)
    - Ejecuta la lógica del agente
    """
    ip = get_remote_address(request)

    # Validar agente
    if agent not in AGENTS:
        logger.error(f"[ROUTER] Agente inválido solicitado | agent={agent} ip={ip}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente no encontrado"
        )

    # Control de acceso según plan
    if agent in PREMIUM_AGENTS and not current_user.is_premium:
        logger.warning(f"[ROUTER] Acceso denegado | user={current_user.id} agent={agent} ip={ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este agente requiere plan premium"
        )

    # Direccionar al agente correcto
    try:
        logger.info(f"[ROUTER] Mensaje dirigido | user={current_user.id} agent={agent} ip={ip}")
        response = AGENTS[agent](message)

        return {
            "agent": agent,
            "message": message,
            "response": response
        }

    except Exception as e:
        logger.error(f"[ROUTER] Error interno | agent={agent} ip={ip} error={e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el router de agentes"
        )
