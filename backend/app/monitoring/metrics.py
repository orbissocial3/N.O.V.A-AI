# backend/app/monitoring/metrics.py
"""
Metrics
-------
Exposición de métricas para Prometheus y monitoreo en N.O.V.A.
Incluye contadores, histogramas, gauges y funciones utilitarias premium.
"""

from prometheus_client import Counter, Histogram, Gauge
from typing import Literal
from datetime import datetime
from app.utils.logger import get_logger

logger = get_logger("metrics")

# --- Contadores ---
REQUEST_COUNT = Counter(
    "nova_requests_total",
    "Número total de requests",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "nova_errors_total",
    "Número total de errores",
    ["endpoint", "severity"]
)

# --- Histogramas ---
REQUEST_LATENCY = Histogram(
    "nova_request_latency_seconds",
    "Latencia de requests",
    ["endpoint"]
)

# --- Gauges ---
ACTIVE_USERS = Gauge(
    "nova_active_users",
    "Número de usuarios activos en el sistema"
)

CONCURRENT_REQUESTS = Gauge(
    "nova_concurrent_requests",
    "Número de requests concurrentes procesándose"
)

# --- Funciones utilitarias ---
def record_request(method: str, endpoint: str) -> None:
    """Registra un request en el contador."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    CONCURRENT_REQUESTS.inc()
    logger.debug(f"[METRICS] Request registrado | method={method} endpoint={endpoint} time={datetime.utcnow().isoformat()}")

def record_error(endpoint: str, severity: Literal["INFO", "WARNING", "ERROR", "CRITICAL"] = "ERROR") -> None:
    """Registra un error en el contador con severidad."""
    ERROR_COUNT.labels(endpoint=endpoint, severity=severity).inc()
    logger.warning(f"[METRICS] Error registrado | endpoint={endpoint} severity={severity} time={datetime.utcnow().isoformat()}")

def record_latency(endpoint: str, duration: float) -> None:
    """Registra la latencia de un request."""
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
    CONCURRENT_REQUESTS.dec()
    logger.debug(f"[METRICS] Latencia registrada | endpoint={endpoint} duration={duration:.4f}s")

def set_active_users(count: int) -> None:
    """Actualiza el número de usuarios activos."""
    ACTIVE_USERS.set(count)
    logger.info(f"[METRICS] Usuarios activos actualizados | count={count}")

def increment_active_users() -> None:
    """Incrementa el número de usuarios activos."""
    ACTIVE_USERS.inc()
    logger.info(f"[METRICS] Usuario activo incrementado")

def decrement_active_users() -> None:
    """Decrementa el número de usuarios activos."""
    ACTIVE_USERS.dec()
    logger.info(f"[METRICS] Usuario activo decrementado")
