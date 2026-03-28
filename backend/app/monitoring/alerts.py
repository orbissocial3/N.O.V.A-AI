# backend/app/monitoring/alerts.py
"""
Alerts
------
Gestión de alertas críticas en N.O.V.A.
Permite enviar notificaciones cuando ocurren eventos importantes.
"""

import logging
from typing import Literal
from app.utils.logger import get_logger

logger = get_logger("alerts")

SeverityLevel = Literal["INFO", "ERROR", "CRITICAL"]

def send_alert(message: str, severity: SeverityLevel = "INFO") -> None:
    """
    Envía una alerta al sistema de logs.
    En producción, aquí se integraría con Slack, Email o PagerDuty.
    :param message: Mensaje de alerta
    :param severity: Nivel de severidad (INFO, ERROR, CRITICAL)
    """
    severity = severity.upper()
    if severity == "CRITICAL":
        logger.critical(f"[ALERT] {message}")
        # Aquí se podría integrar con PagerDuty/Slack/Email
    elif severity == "ERROR":
        logger.error(f"[ALERT] {message}")
    else:
        logger.info(f"[ALERT] {message}")

def alert_error(context: str, error: Exception) -> None:
    """
    Envía una alerta de error con contexto adicional.
    :param context: Contexto donde ocurrió el error
    :param error: Excepción capturada
    """
    send_alert(f"{context} | Error: {error}", severity="ERROR")

def alert_critical(context: str, details: str) -> None:
    """
    Envía una alerta crítica con detalles adicionales.
    :param context: Contexto del evento crítico
    :param details: Detalles del evento
    """
    send_alert(f"{context} | CRITICAL: {details}", severity="CRITICAL")
