# backend/app/middleware/cors.py
"""
CORS Middleware
----------------------------
Configura CORS para N.O.V.A
- Orígenes dinámicos desde settings
- Seguridad reforzada en producción
- Logging de configuración aplicada
"""

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("cors")

def setup_cors(app):
    """
    Configura CORS en la aplicación FastAPI.
    """
    # Orígenes permitidos (usar settings.CORS_ORIGINS en producción)
    allowed_origins = settings.CORS_ALLOWED_ORIGINS or ["http://localhost:3000"]


    # Métodos permitidos
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    # Headers permitidos
    allowed_headers = ["Authorization", "Content-Type", "Accept"]

    # Headers expuestos (para trazabilidad con AuditMiddleware)
    exposed_headers = ["X-Request-ID", "X-Request-Duration"]

    logger.info(
        f"[CORS] Configuración aplicada | Orígenes: {allowed_origins} | "
        f"Métodos: {allowed_methods} | Headers: {allowed_headers}"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
        expose_headers=exposed_headers,
        max_age=600  # cache de preflight en segundos
    )
