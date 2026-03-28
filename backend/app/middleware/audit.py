# backend/app/middleware/audit.py
"""
Audit Middleware
----------------------------
Middleware de Auditoría para N.O.V.A
- Registra inicio y fin de cada petición
- Incluye duración, estado, usuario y headers críticos
- Manejo de errores robusto
- Añade trazabilidad con X-Request-ID
"""

import datetime
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.utils.logger import get_logger

logger = get_logger("audit")

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generar un ID único para la trazabilidad de la petición
        request_id = str(uuid.uuid4())
        start_time = datetime.datetime.utcnow()

        # Extraer información crítica
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        auth_header = request.headers.get("authorization", "none")
        path = request.url.path

        logger.info(
            f"[AUDIT] [{request_id}] Inicio petición: {request.method} {path} "
            f"| Cliente: {client_host} | UA: {user_agent} | Auth: {auth_header}"
        )

        try:
            # Procesar la petición
            response: Response = await call_next(request)
        except Exception as e:
            duration = (datetime.datetime.utcnow() - start_time).total_seconds()
            logger.error(
                f"[AUDIT] [{request_id}] Error en petición: {request.method} {path} "
                f"| Duración: {duration:.3f}s | Error: {e}"
            )
            raise

        # Registrar fin de la petición
        duration = (datetime.datetime.utcnow() - start_time).total_seconds()
        logger.info(
            f"[AUDIT] [{request_id}] Fin petición: {request.method} {path} "
            f"| Duración: {duration:.3f}s | Estado: {response.status_code}"
        )

        # Añadir el ID de auditoría en la respuesta
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Request-Duration"] = f"{duration:.3f}s"

        return response


# Función adicional para auditoría de creación de chats
def log_chat_creation(user_id: str, chat_id: str) -> bool:
    """
    Registra la creación de un chat en los logs de auditoría.
    """
    logger.info(f"[AUDIT] Chat creado - user_id={user_id}, chat_id={chat_id}")
    return True
def log_chat_creation(user_id: str, chat_id: str) -> bool:
    logger.info(f"[AUDIT] Chat creado - user_id={user_id}, chat_id={chat_id}")
    return True
