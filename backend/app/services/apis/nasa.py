"""
nasa.py
-----------------------------------
Servicio de integración con la API oficial de la NASA
- Soporta múltiples endpoints (APOD, Mars Rover, NeoWs, etc.)
- Manejo de errores robusto y logging premium
- Configuración centralizada con settings.NASA_API_KEY
"""

import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("nasa")

class NasaService:
    BASE_URL = "https://api.nasa.gov"

    @staticmethod
    def _request(endpoint: str, params: dict = None) -> dict:
        """
        Método interno para realizar peticiones a la NASA.
        Args:
            endpoint (str): Ruta del endpoint (ej. '/planetary/apod')
            params (dict): Parámetros adicionales
        Returns:
            dict: Respuesta JSON o error
        """
        if params is None:
            params = {}
        params["api_key"] = settings.NASA_API_KEY

        url = f"{NasaService.BASE_URL}{endpoint}"
        logger.info(f"[NASA] Consulta | endpoint={endpoint} | params={params}")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"[NASA] Éxito | endpoint={endpoint}")
            return data
        except requests.exceptions.Timeout:
            logger.error(f"[NASA] Timeout | endpoint={endpoint}")
            return {"error": "Tiempo de espera excedido al consultar NASA"}
        except requests.exceptions.RequestException as e:
            logger.error(f"[NASA] Error HTTP | endpoint={endpoint} | error={e}")
            return {"error": f"Error HTTP al consultar NASA: {str(e)}"}
        except Exception as e:
            logger.error(f"[NASA] Excepción inesperada | endpoint={endpoint} | error={e}")
            return {"error": "Error interno al consultar NASA"}

    # --- Endpoints específicos ---

    @staticmethod
    def get_apod(date: str = None, hd: bool = False) -> dict:
        """
        Imagen Astronómica del Día (APOD).
        Args:
            date (str): Fecha en formato YYYY-MM-DD (opcional).
            hd (bool): Si se desea imagen en alta resolución.
        Returns:
            dict: Datos de la imagen (título, explicación, url).
        """
        params = {}
        if date:
            params["date"] = date
        if hd:
            params["hd"] = "True"

        data = NasaService._request("/planetary/apod", params)
        return {
            "title": data.get("title"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "date": data.get("date"),
            "copyright": data.get("copyright")
        } if "error" not in data else data

    @staticmethod
    def get_mars_rover_photos(rover: str = "curiosity", sol: int = 1000, camera: str = None) -> dict:
        """
        Fotos del Rover en Marte.
        Args:
            rover (str): Nombre del rover ('curiosity', 'opportunity', 'spirit').
            sol (int): Día marciano (sol).
            camera (str): Cámara opcional (ej. 'FHAZ', 'RHAZ', 'NAVCAM').
        Returns:
            dict: Lista de fotos con metadata.
        """
        params = {"sol": sol}
        if camera:
            params["camera"] = camera

        data = NasaService._request(f"/mars-photos/api/v1/rovers/{rover}/photos", params)
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
    def get_neo_feed(start_date: str, end_date: str) -> dict:
        """
        Objetos cercanos a la Tierra (Near Earth Objects).
        Args:
            start_date (str): Fecha inicial YYYY-MM-DD.
            end_date (str): Fecha final YYYY-MM-DD.
        Returns:
            dict: Datos de asteroides detectados.
        """
        params = {"start_date": start_date, "end_date": end_date}
        data = NasaService._request("/neo/rest/v1/feed", params)
        return data if "error" not in data else data
