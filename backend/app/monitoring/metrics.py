# backend/app/monitoring/metrics.py
"""
Metrics
-------
Exposición de métricas para Prometheus y monitoreo en N.O.V.A.
Incluye contadores, histogramas y funciones utilitarias.
"""

from prometheus_client import Counter, Histogram, Gauge
from typing import Literal

# Contadores
REQUEST_COUNT = Counter(
    "nova_requests_total",
    "Número total de requests",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "nova_errors_total",
    "Número total de errores",
    ["endpoint"]
)

# Histogramas
REQUEST_LATENCY = Histogram(
    "nova_request_latency_seconds",
    "Latencia de requests",
    ["endpoint"]
)

# Gauge (estado actual)
ACTIVE_USERS = Gauge(
    "nova_active_users",
    "Número de usuarios activos en el sistema"
)

def record_request(method: str, endpoint: str) -> None:
    """
    Registra un request en el contador.
    """
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

def record_error(endpoint: str) -> None:
    """
    Registra un error en el contador.
    """
    ERROR_COUNT.labels(endpoint=endpoint).inc()

def record_latency(endpoint: str, duration: float) -> None:
    """
    Registra la latencia de un request.
    """
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

def set_active_users(count: int) -> None:
    """
    Actualiza el número de usuarios activos.
    """
    ACTIVE_USERS.set(count)

def increment_active_users() -> None:
    """
    Incrementa el número de usuarios activos.
    """
    ACTIVE_USERS.inc()

def decrement_active_users() -> None:
    """
    Decrementa el número de usuarios activos.
    """
    ACTIVE_USERS.dec()
