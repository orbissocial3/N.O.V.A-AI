# backend/app/monitoring/alerts.py
"""
Alerts
------
Gestión de alertas críticas en N.O.V.A.
Incluye integración futura con Slack, Email o PagerDuty,
trazabilidad, auditoría y métricas.
"""

import logging
from typing import Literal
from datetime import datetime
from app.utils.logger import get_logger
from app.monitoring import metrics, tracing

logger = get_logger("alerts")

SeverityLevel = Literal["INFO", "WARNING", "ERROR", "CRITICAL"]

def send_alert(message: str, severity: SeverityLevel = "INFO", context: str = "system") -> None:
    """
    Envía una alerta al sistema de logs y métricas.
    En producción, aquí se integraría con Slack, Email o PagerDuty.
    
    :param message: Mensaje de alerta
    :param severity: Nivel de severidad (INFO, WARNING, ERROR, CRITICAL)
    :param context: Contexto del evento (ej. 'auth', 'db', 'chat')
    """
    severity = severity.upper()
    timestamp = datetime.utcnow().isoformat()

    # Métricas y trazabilidad
    metrics.record_request("ALERT", f"{context}:{severity}")
    with tracing.start_span(f"alert:{context}:{severity}"):
        if severity == "CRITICAL":
            logger.critical(f"[ALERT] {timestamp} | {context} | {message}")
            # TODO: Integrar con PagerDuty/Slack/Email
        elif severity == "ERROR":
            logger.error(f"[ALERT] {timestamp} | {context} | {message}")
        elif severity == "WARNING":
            logger.warning(f"[ALERT] {timestamp} | {context} | {message}")
        else:
            logger.info(f"[ALERT] {timestamp} | {context} | {message}")

def alert_info(context: str, details: str) -> None:
    """Envía una alerta informativa con contexto adicional."""
    send_alert(f"{context} | INFO: {details}", severity="INFO", context=context)

def alert_warning(context: str, details: str) -> None:
    """Envía una alerta de advertencia con contexto adicional."""
    send_alert(f"{context} | WARNING: {details}", severity="WARNING", context=context)

def alert_error(context: str, error: Exception) -> None:
    """Envía una alerta de error con contexto adicional."""
    send_alert(f"{context} | Error: {error}", severity="ERROR", context=context)

def alert_critical(context: str, details: str) -> None:
    """Envía una alerta crítica con detalles adicionales."""
    send_alert(f"{context} | CRITICAL: {details}", severity="CRITICAL", context=context)
