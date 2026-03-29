# backend/app/services/agents/student.py
"""
Agente Estudiante Premium
-------------------------
Funciones avanzadas:
 - Resúmenes académicos (Wikipedia/Open Library)
 - Explicaciones científicas y matemáticas (Wolfram Alpha)
 - Astronomía y astrología (NASA APIs)
 - Ayuda con tareas y ejercicios prácticos
"""

import os
import requests
from app.utils.logger import get_logger

logger = get_logger("student_agent")

# Endpoints oficiales
WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WOLFRAM_API = "http://api.wolframalpha.com/v1/result"
NASA_API = "https://api.nasa.gov/planetary/apod"
OPENLIBRARY_API = "https://openlibrary.org/search.json"

# -----------------------------
# Funciones de integración
# -----------------------------

def fetch_wikipedia_summary(topic: str) -> str:
    """Obtiene un resumen académico desde Wikipedia."""
    try:
        response = requests.get(WIKIPEDIA_API + topic, timeout=10)
        response.raise_for_status()
        data = response.json()
        extract = data.get("extract")
        if extract:
            return f"📘 Resumen académico sobre *{topic}*:\n{extract}"
        return "No encontré información en Wikipedia."
    except Exception as e:
        logger.error(f"[STUDENT] Error Wikipedia: {e}")
        return "No pude obtener información en Wikipedia en este momento."

def fetch_openlibrary_books(query: str) -> str:
    """Busca referencias académicas en Open Library."""
    try:
        response = requests.get(OPENLIBRARY_API, params={"q": query}, timeout=10)
        response.raise_for_status()
        data = response.json()
        docs = data.get("docs", [])
        if not docs:
            return "No encontré libros relacionados en Open Library."
        titles = [doc.get("title") for doc in docs[:3] if "title" in doc]
        return "📚 Referencias académicas: " + "; ".join(titles)
    except Exception as e:
        logger.error(f"[STUDENT] Error OpenLibrary: {e}")
        return "No pude obtener referencias académicas en este momento."

def fetch_wolfram_answer(query: str) -> str:
    """Resuelve consultas científicas y matemáticas con Wolfram Alpha."""
    try:
        app_id = os.getenv("WOLFRAM_APP_ID")
        if not app_id:
            return "No se configuró la clave de Wolfram Alpha."
        response = requests.get(WOLFRAM_API, params={"i": query, "appid": app_id}, timeout=10)
        response.raise_for_status()
        return f"🔬 Explicación científica:\n{response.text.strip()}"
    except Exception as e:
        logger.error(f"[STUDENT] Error Wolfram: {e}")
        return "No pude resolver la consulta científica."

def fetch_nasa_info() -> str:
    """Obtiene información astronómica desde NASA (APOD)."""
    try:
        api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        response = requests.get(NASA_API, params={"api_key": api_key}, timeout=10)
        response.raise_for_status()
        data = response.json()
        title = data.get("title", "Astronomía")
        explanation = data.get("explanation", "No hay explicación disponible.")
        return f"🌌 {title}:\n{explanation}"
    except Exception as e:
        logger.error(f"[STUDENT] Error NASA: {e}")
        return "No pude obtener información astronómica."

# -----------------------------
# Agente principal
# -----------------------------

def student_agent(message: str) -> str:
    """Procesa el mensaje del usuario y decide qué API usar."""
    msg = message.lower().strip()
    logger.info(f"[STUDENT] Procesando mensaje: {msg}")

    if "resumen" in msg:
        topic = msg.replace("resumen", "").strip() or "Education"
        return fetch_wikipedia_summary(topic)

    elif "libro" in msg or "referencia" in msg:
        query = msg.replace("libro", "").replace("referencia", "").strip() or "Science"
        return fetch_openlibrary_books(query)

    elif "explica" in msg or "explicación" in msg:
        query = msg.replace("explica", "").replace("explicación", "").strip() or "photosynthesis"
        return fetch_wolfram_answer(query)

    elif "astronomía" in msg or "astrología" in msg or "espacio" in msg:
        return fetch_nasa_info()

    elif "tarea" in msg or "ejercicio" in msg:
        return (
            "📝 Plan paso a paso para tu tarea:\n"
            "1️⃣ Analiza el problema.\n"
            "2️⃣ Divide en subtareas.\n"
            "3️⃣ Aplica ejemplos prácticos.\n"
            "4️⃣ Revisa y corrige.\n"
            "5️⃣ Consulta fuentes verificadas si es necesario."
        )

    else:
        return (
            "🎓 Soy tu agente estudiante. Puedo generar resúmenes académicos, "
            "explicaciones científicas y matemáticas, referencias de libros, información astronómica "
            "y ayudarte con tus tareas prácticas."
        )
