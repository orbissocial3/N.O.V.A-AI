# backend/app/services/agents/programmer_premium.py
"""
Agente Programador Premium
--------------------------
Funciones avanzadas:
 - Ejemplos de código en múltiples lenguajes
 - Explicaciones dinámicas (Stack Exchange API)
 - Ejecución de código online (Judge0 API)
 - Debugging inteligente
"""

import random
import requests
import os
from app.utils.logger import get_logger

logger = get_logger("programmer_premium_agent")

JUDGE0_API = "https://judge0-ce.p.rapidapi.com/submissions"
STACK_API = "https://api.stackexchange.com/2.3/search/advanced"

def get_code_example(topic: str, language: str = "python") -> str:
    examples = {
        "python": "for i in range(5):\n    print(i)",
        "javascript": "for(let i=0; i<5; i++) {\n  console.log(i);\n}",
        "java": "for(int i=0; i<5; i++) {\n  System.out.println(i);\n}",
        "c++": "for(int i=0; i<5; i++) {\n  std::cout << i << std::endl;\n}"
    }
    return examples.get(language.lower(), examples["python"])

def run_code(code: str, language_id: int = 71) -> str:
    """
    Ejecuta código usando Judge0 API.
    language_id: 71 = Python, 63 = JavaScript, 62 = Java, 52 = C++
    """
    try:
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }
        payload = {"source_code": code, "language_id": language_id}
        response = requests.post(JUDGE0_API, json=payload, headers=headers)
        if response.status_code == 201:
            return "El código fue enviado a ejecución correctamente."
    except Exception as e:
        logger.error(f"[PROGRAMMER PREMIUM] Error Judge0: {e}")
    return "No pude ejecutar el código."

def fetch_stackoverflow(query: str) -> str:
    try:
        response = requests.get(STACK_API, params={
            "order": "desc",
            "sort": "relevance",
            "q": query,
            "site": "stackoverflow"
        })
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                return f"Respuesta encontrada en StackOverflow: {data['items'][0]['title']}"
    except Exception as e:
        logger.error(f"[PROGRAMMER PREMIUM] Error StackOverflow: {e}")
    return "No encontré una respuesta en StackOverflow."

def programmer_premium_agent(message: str) -> str:
    msg = message.lower()
    logger.info(f"[PROGRAMMER PREMIUM] Procesando mensaje: {msg}")

    if "bucle" in msg or "loop" in msg:
        return f"Aquí tienes ejemplos:\n{get_code_example('loop','python')}\n{get_code_example('loop','javascript')}"

    elif "ejecuta" in msg or "run" in msg:
        return run_code("print('Hola desde Python')", language_id=71)

    elif "error" in msg or "debug" in msg:
        return fetch_stackoverflow(msg)

    else:
        return "Soy tu agente programador premium, puedo generar ejemplos en múltiples lenguajes, ejecutar código online y ayudarte a depurar errores."
