"""
wikimedia.py
-----------------------------------
Servicio de integración con Wikimedia (Wikipedia)
- Soporta múltiples idiomas (es, en, it, fr, de, zh, pt)
- Devuelve resumen, título, enlace y miniatura
- Manejo de errores y logging premium
- Control de acceso: solo el agente 'student' puede invocar
"""

import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("wikipedia")

SUPPORTED_LANGS = {"es", "en", "it", "fr", "de", "zh", "pt"}

class WikipediaService:
    """
    Servicio centralizado para consultas a Wikipedia.
    """

    @staticmethod
    def get_summary(topic: str, lang: str = "es", agent: str = "student") -> dict:
        """
        Obtiene el resumen de un artículo de Wikipedia en el idioma solicitado.
        
        Args:
            topic (str): Título del artículo (ej. 'Teoría_de_la_relatividad')
            lang (str): Código de idioma ('es', 'en', 'it', 'fr', 'de', 'zh', 'pt')
            agent (str): Identificador del agente que invoca (solo 'student' permitido)
        
        Returns:
            dict: Contiene título, extracto, url y miniatura
        """

        # Validar agente autorizado
        if agent != "student":
            logger.warning(f"[WIKIPEDIA] Acceso denegado | agent={agent} | topic={topic}")
            return {"error": "Acceso no autorizado. Solo el agente 'student' puede invocar este servicio."}

        # Validar idioma soportado
        if lang not in SUPPORTED_LANGS:
            logger.error(f"[WIKIPEDIA] Idioma no soportado | lang={lang} | topic={topic}")
            return {"error": f"Idioma '{lang}' no soportado. Idiomas disponibles: {', '.join(SUPPORTED_LANGS)}"}

        # Seleccionar endpoint según idioma
        base_url = settings.WIKIMEDIA_ENDPOINTS.get(lang, settings.WIKIMEDIA_ENDPOINTS["es"])
        url = f"{base_url}{topic}"

        logger.info(f"[WIKIPEDIA] Consulta | agent={agent} | lang={lang} | topic={topic}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = {
                "title": data.get("title"),
                "extract": data.get("extract"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                "thumbnail": data.get("thumbnail", {}).get("source")
            }

            logger.info(f"[WIKIPEDIA] Éxito | agent={agent} | lang={lang} | topic={topic}")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"[WIKIPEDIA] Timeout | agent={agent} | lang={lang} | topic={topic}")
            return {"error": "Tiempo de espera excedido al consultar Wikipedia"}

        except requests.exceptions.RequestException as e:
            logger.error(f"[WIKIPEDIA] Error HTTP | agent={agent} | lang={lang} | topic={topic} | error={e}")
            return {"error": f"Error HTTP al consultar Wikipedia: {str(e)}"}

        except Exception as e:
            logger.error(f"[WIKIPEDIA] Excepción inesperada | agent={agent} | lang={lang} | topic={topic} | error={e}")
            return {"error": "Error interno al consultar Wikipedia"}
