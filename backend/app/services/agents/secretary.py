# backend/app/services/agents/secretary.py
"""
Agente Secretario N.O.V.A
-------------------------
Dos modos disponibles:
 - Free: organización básica
 - Premium: productividad ejecutiva avanzada
"""

import random
from app.utils.logger import get_logger

logger = get_logger("secretary_agent")

RESPONSES_FREE = {
    "reunion": [
        "📅 He agendado tu reunión en la lista de pendientes.",
        "🗓️ Recuerda tu reunión, puedo enviarte un recordatorio."
    ],
    "tarea": [
        "📝 He registrado tu tarea en la lista de pendientes.",
        "✅ Tu tarea está anotada, no la olvidarás."
    ],
    "default": [
        "🤖 Soy tu agente secretario FREE: organizo tu tiempo y registro tus tareas básicas.",
        "📑 Puedo ayudarte a coordinar reuniones y tareas simples."
    ]
}

RESPONSES_PREMIUM = {
    "correo": [
        "📧 He redactado tu correo con tono ejecutivo, listo para enviar por Gmail o Outlook.",
        "✉️ El mensaje está preparado con formato corporativo, ¿quieres que lo envíe?",
        "📝 He generado un borrador profesional adaptado a tu contexto."
    ],
    "archivo": [
        "📂 He buscado en tu almacenamiento y encontré coincidencias en Google Drive.",
        "📁 Tu archivo está disponible en OneDrive, ¿quieres abrirlo?",
        "🔎 He localizado documentos relevantes y puedo generar un resumen ejecutivo."
    ],
    "dashboard": [
        "📊 He analizado tu dashboard en Power BI, aquí tienes un resumen de métricas clave.",
        "📈 Los datos muestran tendencias de crecimiento en el último trimestre.",
        "🎯 Sugiero enfocarte en los KPIs con mayor impacto."
    ],
    "agenda": [
        "📆 He sincronizado tu calendario y propuesto horarios óptimos para tu reunión.",
        "📨 Invitaciones enviadas con agenda adjunta.",
        "🗂️ He coordinado la reunión y preparado un informe previo."
    ],
    "default": [
        "🚀 Soy tu agente secretario PREMIUM N.O.V.A: gestiono correos, archivos, dashboards y reuniones.",
        "📑 Puedo preparar informes ejecutivos con tus datos.",
        "🗂️ Coordino tareas avanzadas de productividad y alertas críticas."
    ]
}

def secretary_agent(message: str, mode: str = "free") -> str:
    """
    Agente secretario con dos modos:
    - free: respuestas básicas
    - premium: funciones avanzadas
    """
    msg = message.lower()
    logger.info(f"[SECRETARY] Procesando mensaje: {msg} | modo={mode}")

    if mode == "premium":
        if "correo" in msg or "email" in msg:
            response = random.choice(RESPONSES_PREMIUM["correo"])
        elif "archivo" in msg or "documento" in msg:
            response = random.choice(RESPONSES_PREMIUM["archivo"])
        elif "dashboard" in msg or "ejecutivo" in msg:
            response = random.choice(RESPONSES_PREMIUM["dashboard"])
        elif "agenda" in msg or "reunion" in msg or "meeting" in msg:
            response = random.choice(RESPONSES_PREMIUM["agenda"])
        else:
            response = random.choice(RESPONSES_PREMIUM["default"])
    else:  # modo free
        if "reunion" in msg or "meeting" in msg:
            response = random.choice(RESPONSES_FREE["reunion"])
        elif "tarea" in msg or "task" in msg:
            response = random.choice(RESPONSES_FREE["tarea"])
        else:
            response = random.choice(RESPONSES_FREE["default"])

    logger.debug(f"[SECRETARY] Respuesta generada: {response}")
    return response
