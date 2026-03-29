"""
wikipedia.py
-----------------------------------
Servicio de integración con Wikimedia (Wikipedia)
- Soporta múltiples idiomas (es, en, it, fr, de, zh, pt)
- Devuelve resumen, título, enlace y miniatura
- Manejo de errores y logging premium
"""

import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("wikipedia")

class WikipediaService:
    """
    Servicio centralizado para consultas a Wikipedia.
    """

    @staticmethod
    def get_summary(topic: str, lang: str = "es") -> dict:
        """
        Obtiene el resumen de un artículo de Wikipedia en el idioma solicitado.
        
        Args:
            topic (str): Título del artículo (ej. 'Teoría_de_la_relatividad')
            lang (str): Código de idioma ('es', 'en', 'it', 'fr', 'de', 'zh', 'pt')
        
        Returns:
            dict: Contiene título, extracto, url y miniatura
        """
        # Seleccionar endpoint según idioma
        base_url = settings.WIKIMEDIA_ENDPOINTS.get(lang, settings.WIKIMEDIA_ENDPOINTS["es"])
        url = f"{base_url}{topic}"

        logger.info(f"[WIKIPEDIA] Consulta | lang={lang} | topic={topic}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # lanza excepción si status != 200
            data = response.json()

            result = {
                "title": data.get("title"),
                "extract": data.get("extract"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                "thumbnail": data.get("thumbnail", {}).get("source")
            }

            logger.info(f"[WIKIPEDIA] Éxito | lang={lang} | topic={topic}")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"[WIKIPEDIA] Timeout | lang={lang} | topic={topic}")
            return {"error": "Tiempo de espera excedido al consultar Wikipedia"}

        except requests.exceptions.RequestException as e:
            logger.error(f"[WIKIPEDIA] Error HTTP | lang={lang} | topic={topic} | error={e}")
            return {"error": f"Error HTTP al consultar Wikipedia: {str(e)}"}

        except Exception as e:
            logger.error(f"[WIKIPEDIA] Excepción inesperada | lang={lang} | topic={topic} | error={e}")
            return {"error": "Error interno al consultar Wikipedia"}
