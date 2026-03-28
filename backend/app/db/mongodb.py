# backend/app/db/mongodb.py
"""
MongoDB Connection
----------------------------
Gestión de conexión con MongoDB para N.O.V.A
- Cliente singleton para evitar múltiples conexiones
- Manejo de errores y logging
- Tipado y utilidades para obtener colecciones
- Funciones de cierre y verificación
"""

import logging
from typing import Optional
from pymongo import MongoClient, errors
from app.config import settings

logger = logging.getLogger("nova.mongodb")

# Cliente global (singleton)
_mongo_client: Optional[MongoClient] = None

def get_mongo_client() -> MongoClient:
    """
    Devuelve el cliente MongoDB global.
    Si no existe, lo inicializa con la URI de settings.
    """
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,                # pool de conexiones
                connect=True
            )
            # Verificar conexión inicial
            _mongo_client.admin.command("ping")
            logger.info("[MongoDB] Conexión establecida correctamente")
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"[MongoDB] Error de conexión (timeout): {e}")
            raise
        except Exception as e:
            logger.error(f"[MongoDB] Error inesperado: {e}")
            raise
    return _mongo_client

def get_database():
    """
    Devuelve la base de datos configurada en settings.
    """
    client = get_mongo_client()
    return client[settings.MONGO_DB]

def get_collection(collection_name: str):
    """
    Devuelve una colección específica de la base de datos.
    :param collection_name: Nombre de la colección
    :return: Objeto Collection
    """
    db = get_database()
    return db[collection_name]

def close_mongo_connection():
    """
    Cierra la conexión global con MongoDB.
    """
    global _mongo_client
    if _mongo_client:
        try:
            _mongo_client.close()
            logger.info("[MongoDB] Conexión cerrada")
        except Exception as e:
            logger.error(f"[MongoDB] Error al cerrar conexión: {e}")
        finally:
            _mongo_client = None

def test_mongo_connection() -> bool:
    """
    Verifica si MongoDB está accesible.
    :return: True si responde al ping, False si no
    """
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True
    except Exception as e:
        logger.error(f"[MongoDB] Ping fallido: {e}")
        return False
