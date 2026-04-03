"""
nasa.py
-----------------------------------
Servicio de integración con la API oficial de la NASA
- Soporta múltiples endpoints (APOD, Mars Rover, NeoWs, etc.)
- Manejo de errores robusto y logging premium
- Configuración centralizada con settings.NASA_API_KEY
- Control de acceso: solo el agente 'student' puede invocar
"""

import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("nasa")

class NasaService:
    BASE_URL = "https://api.nasa.gov"

    @staticmethod
    def _request(endpoint: str, params: dict = None, agent: str = "student") -> dict:
        """
        Método interno para realizar peticiones a la NASA.
        Args:
            endpoint (str): Ruta del endpoint (ej. '/planetary/apod')
            params (dict): Parámetros adicionales
            agent (str): Identificador del agente que invoca (solo 'student' permitido)
        Returns:
            dict: Respuesta JSON o error
        """
        if agent != "student":
            logger.warning(f"[NASA] Acceso denegado | agent={agent} | endpoint={endpoint}")
            return {"error": "Acceso no autorizado. Solo el agente 'student' puede invocar este servicio."}

        if params is None:
            params = {}
        params["api_key"] = settings.NASA_API_KEY

        url = f"{NasaService.BASE_URL}{endpoint}"
        logger.info(f"[NASA] Consulta | agent={agent} | endpoint={endpoint} | params={params}")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"[NASA] Éxito | agent={agent} | endpoint={endpoint}")
            return data
        except requests.exceptions.Timeout:
            logger.error(f"[NASA] Timeout | agent={agent} | endpoint={endpoint}")
            return {"error": "Tiempo de espera excedido al consultar NASA"}
        except requests.exceptions.RequestException as e:
            logger.error(f"[NASA] Error HTTP | agent={agent} | endpoint={endpoint} | error={e}")
            return {"error": f"Error HTTP al consultar NASA: {str(e)}"}
        except Exception as e:
            logger.error(f"[NASA] Excepción inesperada | agent={agent} | endpoint={endpoint} | error={e}")
            return {"error": "Error interno al consultar NASA"}

    # --- Endpoints específicos ---

    @staticmethod
    def get_apod(date: str = None, hd: bool = False, agent: str = "student") -> dict:
        """
        Imagen Astronómica del Día (APOD).
        Args:
            date (str): Fecha en formato YYYY-MM-DD (opcional).
            hd (bool): Si se desea imagen en alta resolución.
            agent (str): Agente invocador (solo 'student')
        Returns:
            dict: Datos de la imagen (título, explicación, url).
        """
        params = {}
        if date:
            params["date"] = date
        if hd:
            params["hd"] = "True"

        data = NasaService._request("/planetary/apod", params, agent)
        return {
            "title": data.get("title"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "date": data.get("date"),
            "copyright": data.get("copyright")
        } if "error" not in data else data

    @staticmethod
    def get_mars_rover_photos(rover: str = "curiosity", sol: int = 1000, camera: str = None, agent: str = "student") -> dict:
        """
        Fotos del Rover en Marte.
        Args:
            rover (str): Nombre del rover ('curiosity', 'opportunity', 'spirit').
            sol (int): Día marciano (sol).
            camera (str): Cámara opcional (ej. 'FHAZ', 'RHAZ', 'NAVCAM').
            agent (str): Agente invocador (solo 'student')
        Returns:
            dict: Lista de fotos con metadata.
        """
        params = {"sol": sol}
        if camera:
            params["camera"] = camera

        data = NasaService._request(f"/mars-photos/api/v1/rovers/{rover}/photos", params, agent)
        return {
            "rover": rover,
            "sol": sol,
            "photos": [
                {
                    "id": photo.get("id"),
                    "img_src": photo.get("img_src"),
                    "earth_date": photo.get("earth_date"),
                    "camera": photo.get("camera", {}).get("full_name")
                }
                for photo in data.get("photos", [])
            ]
        } if "error" not in data else data

    @staticmethod
    def get_neo_feed(start_date: str, end_date: str, agent: str = "student") -> dict:
        """
        Objetos cercanos a la Tierra (Near Earth Objects).
        Args:
            start_date (str): Fecha inicial YYYY-MM-DD.
            end_date (str): Fecha final YYYY-MM-DD.
            agent (str): Agente invocador (solo 'student')
        Returns:
            dict: Datos de asteroides detectados.
        """
        params = {"start_date": start_date, "end_date": end_date}
        data = NasaService._request("/neo/rest/v1/feed", params, agent)
        return data if "error" not in data else data
