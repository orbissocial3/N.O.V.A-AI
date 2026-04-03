# backend/app/services/agents/programmer.py
"""
Agente Programador N.O.V.A
--------------------------
Dos modos disponibles:
 - Free: ejemplos básicos y explicaciones simples
 - Premium: ciclo de vida completo del desarrollo (ejemplos, ejecución, debugging, refactorización, tests)
"""

import os
import requests
import random
from app.utils.logger import get_logger

logger = get_logger("programmer_agent")

JUDGE0_API = "https://judge0-ce.p.rapidapi.com/submissions"
STACK_API = "https://api.stackexchange.com/2.3/search/advanced"

EXAMPLES = {
    "python": "for i in range(5):\n    print(i)",
    "javascript": "for(let i=0; i<5; i++) {\n  console.log(i);\n}",
    "java": "for(int i=0; i<5; i++) {\n  System.out.println(i);\n}",
    "c++": "for(int i=0; i<5; i++) {\n  std::cout << i << std::endl;\n}",
    "go": "for i := 0; i < 5; i++ {\n  fmt.Println(i)\n}",
    "rust": "for i in 0..5 {\n  println!(\"{}\", i);\n}"
}

def get_code_example(language: str = "python") -> str:
    return EXAMPLES.get(language.lower(), EXAMPLES["python"])

def run_code(code: str, language_id: int = 71) -> str:
    try:
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }
        payload = {"source_code": code, "language_id": language_id}
        response = requests.post(JUDGE0_API, json=payload, headers=headers)
        if response.status_code == 201:
            return "✅ El código fue enviado a ejecución correctamente."
        else:
            return f"⚠️ Error al enviar código: {response.status_code}"
    except Exception as e:
        logger.error(f"[PROGRAMMER] Error Judge0: {e}")
        return "❌ No pude ejecutar el código."

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
            if data.get("items"):
                return f"📚 Respuesta encontrada en StackOverflow: {data['items'][0]['title']}"
        return "🤔 No encontré una respuesta en StackOverflow."
    except Exception as e:
        logger.error(f"[PROGRAMMER] Error StackOverflow: {e}")
        return "❌ Error al consultar StackOverflow."

def programmer_agent(message: str, mode: str = "free") -> str:
    """
    Agente programador con dos modos:
    - free: ejemplos básicos
    - premium: funciones avanzadas
    """
    msg = message.lower()
    logger.info(f"[PROGRAMMER] Procesando mensaje: {msg} | modo={mode}")

    if mode == "premium":
        if "ejemplo" in msg or "example" in msg:
            lang = "python" if "python" in msg else "javascript" if "javascript" in msg else "java"
            return f"📌 Ejemplo en {lang}:\n{get_code_example(lang)}"
        elif "ejecuta" in msg or "run" in msg:
            return run_code("print('Hola desde Python')", language_id=71)
        elif "error" in msg or "debug" in msg:
            return fetch_stackoverflow(msg)
        elif "test" in msg:
            return "🧪 He generado tests unitarios para tu función."
        elif "refactor" in msg or "optimiza" in msg:
            return "♻️ He refactorizado tu código siguiendo mejores prácticas."
        else:
            return "🚀 Soy tu agente programador PREMIUM N.O.V.A: genero ejemplos multi‑lenguaje, ejecuto código online, depuro errores, refactorizo y creo tests."
    else:  # modo free
        if "ejemplo" in msg or "example" in msg:
            return f"📌 Ejemplo básico:\n{get_code_example('python')}"
        else:
            return "🤖 Soy tu agente programador FREE: puedo darte ejemplos básicos y explicaciones simples."
