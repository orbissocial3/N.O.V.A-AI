# backend/app/monitoring/tracing.py
"""
Tracing
-------
Configuración de OpenTelemetry para trazabilidad distribuida en N.O.V.A.
Incluye configuración del proveedor, exportador OTLP (gRPC) y utilidades para spans.
Modo dual:
- En producción: usa OTLP gRPC exporter
- En desarrollo/tests: usa ConsoleSpanExporter para evitar incompatibilidades
"""

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode

from app.utils.logger import get_logger

logger = get_logger("tracing")

# Configurar recurso con metadatos del servicio
resource = Resource.create({
    "service.name": "nova-backend",
    "service.version": os.getenv("APP_VERSION", "1.0.0"),
    "deployment.environment": os.getenv("ENVIRONMENT", "development")
})

# Configurar proveedor de trazas
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Detectar entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    # Exportador OTLP gRPC (ej. Jaeger, Tempo, Grafana)
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317"),
        insecure=os.getenv("OTLP_INSECURE", "true").lower() == "true"
    )
else:
    # Exportador simple a consola (para desarrollo/tests)
    otlp_exporter = ConsoleSpanExporter()

# Procesador de spans (batch para eficiencia)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

# Tracer global
tracer = trace.get_tracer("nova-tracer")

def start_span(name: str, attributes: dict | None = None):
    """
    Inicia un span para trazabilidad.
    Uso recomendado: con 'with' para asegurar cierre automático.
    :param name: Nombre del span
    :param attributes: Diccionario de atributos adicionales
    """
    span_ctx = tracer.start_as_current_span(name)
    if attributes:
        for key, value in attributes.items():
            span_ctx.__enter__().set_attribute(key, value)
    return span_ctx

def trace_function(name: str):
    """
    Decorador para trazar funciones automáticamente.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with start_span(name, {"function": func.__name__}) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR))
                    logger.error(f"[TRACING] Error en función {func.__name__}: {e}")
                    raise
        return wrapper
    return decorator

def get_tracer() -> trace.Tracer:
    """
    Devuelve el tracer global configurado.
    """
    return tracer
