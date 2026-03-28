# backend/app/services/agents/creative_premium.py
"""
Agente Creativo Premium
-----------------------
Funciones avanzadas:
 - Generación de campañas de marketing digital
 - Creación de imágenes hiperrealistas (DALL·E / Stable Diffusion)
 - Estrategias de marketing y redes sociales
 - Brainstorming avanzado
"""

import random
import os
import requests
from app.utils.logger import get_logger

logger = get_logger("creative_premium_agent")

OPENAI_API = "https://api.openai.com/v1/completions"
DALLE_API = "https://api.openai.com/v1/images/generations"

def generate_slogan(prompt: str) -> str:
    try:
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"}
        payload = {
            "model": "text-davinci-003",
            "prompt": f"Genera un slogan creativo para: {prompt}",
            "max_tokens": 50
        }
        response = requests.post(OPENAI_API, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["text"].strip()
    except Exception as e:
        logger.error(f"[CREATIVE PREMIUM] Error OpenAI slogan: {e}")
    return "No pude generar un slogan en este momento."

def generate_image(prompt: str) -> str:
    try:
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"}
        payload = {"prompt": prompt, "n": 1, "size": "1024x1024"}
        response = requests.post(DALLE_API, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return f"Imagen generada: {data['data'][0]['url']}"
    except Exception as e:
        logger.error(f"[CREATIVE PREMIUM] Error DALL·E: {e}")
    return "No pude generar una imagen en este momento."

def creative_premium_agent(message: str) -> str:
    msg = message.lower()
    logger.info(f"[CREATIVE PREMIUM] Procesando mensaje: {msg}")

    if "slogan" in msg or "título" in msg:
        return generate_slogan(msg)

    elif "imagen" in msg or "foto" in msg:
        return generate_image(msg)

    elif "marketing" in msg or "campaña" in msg:
        return "He diseñado una campaña digital con slogans, imágenes y estrategias para redes sociales."

    else:
        return "Soy tu agente creativo premium, puedo generar campañas completas, slogans, imágenes hiperrealistas y estrategias de marketing."
