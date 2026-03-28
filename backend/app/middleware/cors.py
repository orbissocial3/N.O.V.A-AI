# backend/app/middleware/cors.py
"""
CORS Middleware
----------------------------
Configura CORS para N.O.V.A
- Orígenes dinámicos desde settings
- Seguridad reforzada en producción
- Logging, métricas y trazabilidad
"""

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logger import get_logger
from app.monitoring import metrics, tracing, alerts

logger = get_logger("cors")

def setup_cors(app):
    """
    Configura CORS en la aplicación FastAPI.
    """
    # Orígenes permitidos (usar settings.CORS_ALLOWED_ORIGINS en producción)
    allowed_origins = settings.CORS_ALLOWED_ORIGINS or ["http://localhost:3000"]

    # Validación estricta en producción
    if settings.ENVIRONMENT == "production":
        if not allowed_origins or "http://localhost:3000" in allowed_origins:
            alerts.send_alert("⚠️ Configuración insegura de CORS detectada en producción", severity="CRITICAL")
            logger.critical("[CORS] Configuración insegura detectada: localhost permitido en producción")

    # Métodos permitidos
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    # Headers permitidos
    allowed_headers = ["Authorization", "Content-Type", "Accept"]

    # Headers expuestos (para trazabilidad con AuditMiddleware)
    exposed_headers = ["X-Request-ID", "X-Request-Duration"]

    # Logging enriquecido
    logger.info(
        f"[CORS] Configuración aplicada | Orígenes: {allowed_origins} | "
        f"Métodos: {allowed_methods} | Headers: {allowed_headers} | Expuestos: {exposed_headers}"
    )

    # Métricas y trazabilidad
    metrics.record_request("CONFIG", "CORS")
    with tracing.start_span("middleware:cors"):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=allowed_methods,
            allow_headers=allowed_headers,
            expose_headers=exposed_headers,
            max_age=600  # cache de preflight en segundos
        )
