# backend/app/routes/chat.py
"""
Rutas de Chat
-------------
Gestión de conversaciones entre usuarios y agentes IA.
Incluye autenticación, rate limits, logging, auditoría, métricas,
trazabilidad, alertas y persistencia con caché.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.postgresql import get_db
from app.models.chat import Chat
from app.models.agent import Agent
from app.models.user import User
from app.utils.security import get_current_user
from app.utils.rate_limits import check_rate_limit
from app.utils.logger import get_logger

# Auditoría, métricas, trazabilidad y alertas
from app.middleware.audit import log_chat_creation
from app.monitoring import metrics, tracing, alerts
from app.cache.redis_cache import set_cache, get_cache, delete_cache

# Importar servicios de agentes IA
from app.services.agents.student import student_agent
from app.services.agents.programmer import programmer_agent
from app.services.agents.secretary import secretary_agent
from app.services.agents.investor import investor_agent
from app.services.agents.creative import creative_agent

import datetime, time

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "No encontrado"}}
)

logger = get_logger("chat")

# --- Obtener historial de chats ---
@router.get("/{user_id}")
def get_user_chats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve el historial de chats de un usuario.
    Solo accesible por el propio usuario o un administrador.
    """
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    chats = db.query(Chat).filter(Chat.user_id == user_id).all()
    logger.info(f"[CHAT] Historial consultado | user={user.email} total={len(chats)}")

    # Métricas
    metrics.record_request("GET", "/chat/{user_id}")

    return [chat.to_dict() for chat in chats]

# --- Crear un nuevo chat ---
@router.post("/")
def create_chat(
    user_id: int,
    agent_id: int,
    message: str
):
    """
    Versión simplificada para pruebas.
    No requiere autenticación ni base de datos.
    """
    # Seleccionar agente IA
    agent_map = {
        1: student_agent,
        2: programmer_agent,
        3: secretary_agent,
        4: investor_agent,
        5: creative_agent
    }

    agent_fn = agent_map.get(agent_id, None)

    if not agent_fn:
        return {"error": "Agente no reconocido"}

    response = agent_fn(message)

    return {
        "user_id": user_id,
        "agent_id": agent_id,
        "message": message,
        "response": response
    }

    # Seleccionar agente IA
    agent_name = agent.name.lower()
    with tracing.start_span(f"chat:{agent_name}"):
        try:
            if agent_name == "estudiante":
                response = student_agent(message)
            elif agent_name == "programador":
                response = programmer_agent(message)
            elif agent_name == "secretario":
                response = secretary_agent(message)
            elif agent_name == "inversor":
                response = investor_agent(message)
            elif agent_name == "creativo":
                response = creative_agent(message)
            else:
                response = "Agente no reconocido."

            # Guardar chat en DB
            chat = Chat(
                user_id=user.id,
                agent_id=agent.id,
                message=message,
                response=response,
                status="sent",
                content_type="text",
                language="es",
                tokens_used=len(message.split()),  # métrica simple de tokens
                created_at=datetime.datetime.utcnow()
            )
            db.add(chat)
            db.commit()
            db.refresh(chat)

            # Auditoría
            log_chat_creation(user=user, chat=chat, db=db)

            # Cachear respuesta
            set_cache(f"chat:{chat.id}", chat.response)

            # Métricas
            metrics.record_request("POST", endpoint)
            metrics.record_latency(endpoint, time.time() - start)

            logger.info(f"[CHAT] Nuevo chat creado | user={user.email} agent={agent.name}")

            return chat.to_dict()
        except Exception as e:
            metrics.record_error(endpoint)
            alerts.send_alert(f"Error creando chat: {str(e)}", severity="CRITICAL")
            logger.error(f"[CHAT] Error al crear chat | user={user_id} agent={agent_id} error={e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creando chat")
