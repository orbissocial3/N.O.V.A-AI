"""
Archivo principal de la aplicación N.O.V.A
------------------------------------------
Inicializa el servidor FastAPI, configura middlewares de seguridad,
auditoría, métricas, trazabilidad y alertas, carga las rutas principales
y define el punto de entrada de la API.
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

# --- Selección dinámica de rutas según modo ---
TESTING = os.getenv("TESTING", "false").lower() == "true"

if TESTING:
    from app.routes import auth as auth_router
    from app.routes import chat as chat_router
else:
    from app.routes import auth_full as auth_router
    from app.routes import chat_full as chat_router

# Rutas que no cambian
from app.routes import plans, agents, admin

# Configuración de logging global
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NOVA")

# Crear instancia de FastAPI con metadatos
app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de Inteligencia Artificial con agentes especializados (Estudiante, Programador, Secretario, Inversor, Creativo).",
    version=settings.APP_VERSION,
    contact={
        "name": "N.O.V.A Support",
        "url": "https://nova.ai/support",
        "email": "support@nova.ai",
    },
    license_info={
        "name": "Propietario N.O.V.A",
        "url": "https://nova.ai/license",
    },
)

# --- Middlewares ---
app.add_middleware(AuditMiddleware)  # Auditoría de todas las peticiones
setup_cors(app)  # Configuración de CORS

# --- Middleware de métricas y trazabilidad ---
@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method

    metrics.record_request(method, endpoint)

    with tracing.start_span(f"{method} {endpoint}"):
        try:
            response = await call_next(request)
        except Exception as exc:
            metrics.record_error(endpoint)
            alerts.send_alert(f"Error en {endpoint}: {str(exc)}", severity="ERROR")
            logger.error(f"[MONITORING] Error en {endpoint}: {exc}")
            raise

    duration = time.time() - start_time
    metrics.record_latency(endpoint, duration)

    return response

# --- Manejo global de excepciones ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error en {request.url}: {str(exc)}")
    alerts.send_alert(f"Excepción global en {request.url}: {str(exc)}", severity="CRITICAL")
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "details": str(exc)},
    )

# --- Rutas dinámicas ---
app.include_router(auth_router.router)
app.include_router(chat_router.router)

# --- Rutas fijas ---
app.include_router(plans.router)
app.include_router(agents.router)
app.include_router(admin.router)

# --- Endpoints básicos ---
@app.get("/")
def root():
    return {"message": f"Bienvenido a {settings.APP_NAME} - Plataforma de Inteligencia Artificial"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.APP_VERSION}

# --- Eventos de ciclo de vida ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 N.O.V.A iniciado correctamente")
    logger.info(f"Configuración cargada: entorno={settings.ENVIRONMENT}, DB={settings.POSTGRES_URL}")
    alerts.send_alert("Servidor iniciado", severity="INFO")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 N.O.V.A detenido")
    alerts.send_alert("Servidor detenido", severity="INFO")
