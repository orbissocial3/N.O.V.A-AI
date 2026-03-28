"""
Rutas de Chat
-------------
Gestión de conversaciones entre usuarios y agentes IA.
Versión simplificada para pruebas (pytest).
"""

from fastapi import APIRouter
from pydantic import BaseModel

# Importar servicios de agentes IA
from app.services.agents.student import student_agent
from app.services.agents.programmer import programmer_agent
from app.services.agents.secretary import secretary_agent
from app.services.agents.investor import investor_agent
from app.services.agents.creative import creative_agent

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "No encontrado"}}
)

# ------------------------------
# MODELO PARA PETICIONES DE CHAT
# ------------------------------

class ChatRequest(BaseModel):
    user_id: int
    agent_id: int
    message: str

# ------------------------------
# ENDPOINT SIMPLIFICADO PARA TESTS
# ------------------------------

@router.post("/")
def create_chat(data: ChatRequest):
    """
    Endpoint simplificado para pytest.
    No requiere autenticación, DB, auditoría ni trazabilidad.
    """

    agent_map = {
        1: student_agent,
        2: programmer_agent,
        3: secretary_agent,
        4: investor_agent,
        5: creative_agent
    }

    agent_fn = agent_map.get(data.agent_id)
    if not agent_fn:
        return {"error": "Agente no reconocido"}

    response = agent_fn(data.message)

    return {
        "user_id": data.user_id,
        "agent_id": data.agent_id,
        "message": data.message,
        "response": response
    }

