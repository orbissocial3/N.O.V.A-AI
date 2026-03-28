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

# Configurar recurso con metadatos del servicio
resource = Resource.create({"service.name": "nova-backend"})

# Configurar proveedor de trazas
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Detectar entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    # Exportador OTLP gRPC (ej. Jaeger, Tempo, Grafana)
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="localhost:4317",  # configurable en settings
        insecure=True               # desactiva TLS si usas localhost
    )
else:
    # Exportador simple a consola (para desarrollo/tests)
    otlp_exporter = ConsoleSpanExporter()

# Procesador de spans (batch para eficiencia)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

# Tracer global
tracer = trace.get_tracer("nova-tracer")

def start_span(name: str):
    """
    Inicia un span para trazabilidad.
    Uso recomendado: con 'with' para asegurar cierre automático.
    """
    return tracer.start_as_current_span(name)

def trace_function(name: str):
    """
    Decorador para trazar funciones automáticamente.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with start_span(name) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR))
                    raise
        return wrapper
    return decorator

def get_tracer() -> trace.Tracer:
    """
    Devuelve el tracer global configurado.
    """
    return tracer
