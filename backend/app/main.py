"""
Archivo principal de la aplicación N.O.V.A
------------------------------------------
El director de orquesta: inicializa FastAPI, configura seguridad,
observabilidad, resiliencia y carga las rutas maestras.
"""

import logging
import time
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Configuración global
from app.config import settings

# Middlewares
from app.middleware.audit import AuditMiddleware
from app.middleware.cors import setup_cors

# Monitoring
from app.monitoring import alerts, metrics, tracing

# Selección dinámica de rutas
TESTING = os.getenv("TESTING", "false").lower() == "true"
if TESTING:
    from app.routes import auth as auth_router
    from app.routes import chat as chat_router
else:
    from app.routes import auth_full as auth_router
    from backend.app.routes import chat as chat_router

# Rutas fijas
from app.routes import plans, agents, admin

# Logging global
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(settings.LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger("NOVA")

# Seguridad extra: Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

# Crear instancia FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de IA con agentes especializados (Estudiante, Programador, Secretario, Inversor, Creativo).",
    version=settings.APP_VERSION,
    contact={"name": "N.O.V.A Support", "url": "https://nova.ai/support", "email": "support@nova.ai"},
    license_info={"name": "Propietario N.O.V.A", "url": "https://nova.ai/license"},
    docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
    openapi_url=None if settings.ENVIRONMENT == "production" else "/openapi.json",
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"[SECURITY] Rate limit excedido | ip={get_remote_address(request)} endpoint={request.url.path}")
    alerts.send_alert(f"Rate limit excedido en {request.url.path}", severity="WARNING")
    return JSONResponse(status_code=429, content={"error": "Demasiados intentos, espera antes de volver a intentar."})

# Middlewares
app.add_middleware(AuditMiddleware)
setup_cors(app)

# Monitoring middleware
@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method
    metrics.record_request(method, endpoint)

    with tracing.start_span(f"{method} {endpoint}", {"ip": get_remote_address(request)}):
        try:
            response = await call_next(request)
        except Exception as exc:
            metrics.record_error(endpoint, severity="ERROR")
            alerts.send_alert(f"Error en {endpoint}: {str(exc)}", severity="ERROR", context="middleware")
            logger.error(f"[MONITORING] Error en {endpoint}: {exc}")
            return JSONResponse(status_code=500, content={"error": "Error interno del servidor"})
    duration = time.time() - start_time
    metrics.record_latency(endpoint, duration)
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error en {request.url}: {str(exc)}")
    alerts.send_alert(f"Excepción global en {request.url}: {str(exc)}", severity="CRITICAL", context="global")
    return JSONResponse(status_code=500, content={"error": "Error interno del servidor", "details": str(exc)})

# Rutas dinámicas
app.include_router(auth_router.router)
app.include_router(chat_router.router)

# Rutas fijas
app.include_router(plans.router)
app.include_router(agents.router)
app.include_router(admin.router)

# Endpoints básicos
@app.get("/")
def root():
    return {"message": f"Bienvenido a {settings.APP_NAME} - El director de orquesta de la IA"}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "db": "connected" if settings.POSTGRES_URL else "not configured",
        "agents": ["student", "programmer", "secretary", "investor", "creative"]
    }

# Eventos ciclo de vida
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 N.O.V.A iniciado correctamente")
    alerts.send_alert("Servidor iniciado", severity="INFO", context="lifecycle")
    metrics.set_active_users(0)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 N.O.V.A detenido")
    alerts.send_alert("Servidor detenido", severity="INFO", context="lifecycle")
