# backend/app/services/agents/student_premium.py
"""
Agente Estudiante Premium
-------------------------
Funciones avanzadas:
 - Resúmenes académicos (Wikipedia/Open Library)
 - Explicaciones científicas y matemáticas (Wolfram Alpha)
 - Astronomía y astrología (NASA APIs)
 - Ayuda con tareas y ejercicios prácticos
"""

import random
import os
import requests
from app.utils.logger import get_logger

logger = get_logger("student_premium_agent")

WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WOLFRAM_API = "http://api.wolframalpha.com/v1/result"
NASA_API = "https://api.nasa.gov/planetary/apod"

def fetch_wikipedia_summary(topic: str) -> str:
    try:
        response = requests.get(WIKIPEDIA_API + topic)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No encontré información en Wikipedia.")
    except Exception as e:
        logger.error(f"[STUDENT PREMIUM] Error Wikipedia: {e}")
    return "No pude obtener información en este momento."

def fetch_wolfram_answer(query: str) -> str:
    try:
        app_id = os.getenv("WOLFRAM_APP_ID")
        response = requests.get(WOLFRAM_API, params={"i": query, "appid": app_id})
        if response.status_code == 200:
            return response.text
    except Exception as e:
        logger.error(f"[STUDENT PREMIUM] Error Wolfram: {e}")
    return "No pude resolver la consulta científica."

def fetch_nasa_info() -> str:
    try:
        api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        response = requests.get(NASA_API, params={"api_key": api_key})
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('title')}: {data.get('explanation')}"
    except Exception as e:
        logger.error(f"[STUDENT PREMIUM] Error NASA: {e}")
    return "No pude obtener información astronómica."

def student_premium_agent(message: str) -> str:
    msg = message.lower()
    logger.info(f"[STUDENT PREMIUM] Procesando mensaje: {msg}")

    if "resumen" in msg:
        topic = msg.replace("resumen", "").strip()
        return fetch_wikipedia_summary(topic or "Education")

    elif "explica" in msg or "explicación" in msg:
        query = msg.replace("explica", "").replace("explicación", "").strip()
        return fetch_wolfram_answer(query or "photosynthesis")

    elif "astronomía" in msg or "astrología" in msg:
        return fetch_nasa_info()

    elif "tarea" in msg:
        return "He generado un plan paso a paso para tu tarea: 1) Analiza el problema, 2) Divide en subtareas, 3) Aplica ejemplos prácticos, 4) Revisa y corrige."

    else:
        return "Soy tu agente estudiante premium, puedo generar resúmenes, explicaciones científicas, información astronómica y ayudarte con tus tareas."
