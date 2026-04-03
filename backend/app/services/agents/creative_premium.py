# backend/app/services/agents/creative_premium.py
"""
Agente Creativo Premium N.O.V.A
-------------------------------
Funciones avanzadas:
 - Generación de campañas de marketing digital
 - Creación de imágenes hiperrealistas (DALL·E / Stable Diffusion)
 - Estrategias de marketing y redes sociales
 - Brainstorming avanzado y storytelling
"""

import random
import os
import requests
from app.utils.logger import get_logger

logger = get_logger("creative_premium_agent")

OPENAI_API = "https://api.openai.com/v1/completions"
DALLE_API = "https://api.openai.com/v1/images/generations"

# -----------------------------
# Funciones de integración
# -----------------------------

def generate_slogan(prompt: str) -> str:
    """Genera un slogan creativo usando OpenAI."""
    try:
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"}
        payload = {
            "model": "text-davinci-003",
            "prompt": f"Genera un slogan creativo, memorable y poderoso para: {prompt}",
            "max_tokens": 60
        }
        response = requests.post(OPENAI_API, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["text"].strip()
    except Exception as e:
        logger.error(f"[CREATIVE PREMIUM] Error OpenAI slogan: {e}")
        return "No pude generar un slogan en este momento."

def generate_image(prompt: str) -> str:
    """Genera una imagen hiperrealista usando DALL·E."""
    try:
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"}
        payload = {"prompt": prompt, "n": 1, "size": "1024x1024"}
        response = requests.post(DALLE_API, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        return f"🎨 Imagen generada: {data['data'][0]['url']}"
    except Exception as e:
        logger.error(f"[CREATIVE PREMIUM] Error DALL·E: {e}")
        return "No pude generar una imagen en este momento."

def generate_campaign(prompt: str) -> str:
    """Diseña una campaña de marketing digital completa."""
    ideas = [
        f"📢 Campaña digital para {prompt}:\n- Slogan impactante\n- Imágenes hiperrealistas\n- Estrategia en Instagram, TikTok y LinkedIn\n- Storytelling emocional\n- Plan de anuncios segmentados",
        f"🚀 Estrategia creativa para {prompt}:\n- Video viral en TikTok\n- Infografías en Instagram\n- Blog posts optimizados SEO\n- Email marketing con storytelling\n- Influencers clave en el sector"
    ]
    return random.choice(ideas)

def brainstorming(prompt: str) -> str:
    """Genera ideas creativas y disruptivas."""
    ideas = [
        f"💡 Brainstorming para {prompt}:\n1️⃣ Concepto futurista\n2️⃣ Narrativa emocional\n3️⃣ Visuales artísticos\n4️⃣ Estrategia viral\n5️⃣ Experiencia inmersiva",
        f"🔥 Ideas disruptivas para {prompt}:\n- Campaña con realidad aumentada\n- Storytelling interactivo\n- Gamificación en redes sociales\n- Arte digital colaborativo\n- Experiencia multisensorial"
    ]
    return random.choice(ideas)

# -----------------------------
# Agente principal
# -----------------------------

def creative_premium_agent(message: str) -> str:
    """Procesa el mensaje del usuario y devuelve creatividad premium."""
    msg = message.lower()
    logger.info(f"[CREATIVE PREMIUM] Procesando mensaje: {msg}")

    if "slogan" in msg or "título" in msg:
        return generate_slogan(msg)

    elif "imagen" in msg or "foto" in msg or "visual" in msg:
        return generate_image(msg)

    elif "marketing" in msg or "campaña" in msg:
        return generate_campaign(msg)

    elif "idea" in msg or "brainstorm" in msg or "creativo" in msg:
        return brainstorming(msg)

    else:
        return (
            "👑 Soy tu agente creativo PREMIUM N.O.V.A: el rey del marketing y las ideas.\n"
            "🎨 Genero campañas hipercompletas, slogans memorables, imágenes hiperrealistas y estrategias de redes sociales.\n"
            "🔥 Soy el cerebro creativo del mundo, el sello de lo bello que es el arte."
        )
