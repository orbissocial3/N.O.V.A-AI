# backend/app/db/redis.py
"""
Redis Connection
----------------------------
Gestión de conexión con Redis para N.O.V.A
- Cliente singleton para evitar múltiples conexiones
- Manejo de errores y logging
- Tipado y utilidades adicionales
"""

import logging
import redis
from typing import Optional
from app.config import settings

logger = logging.getLogger("nova.redis")

# Cliente global (singleton)
_redis_client: Optional[redis.Redis] = None

def get_redis_client() -> redis.Redis:
    """
    Devuelve el cliente Redis global.
    Si no existe, lo inicializa con la configuración de settings.
    """
    global _redis_client
    if _redis_client is None:
        try:
            # Usamos REDIS_URL directamente desde config.py
            _redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,          # devuelve strings en lugar de bytes
                socket_timeout=5,               # timeout de conexión
                socket_connect_timeout=5,
                health_check_interval=30,       # verificación periódica
                retry_on_timeout=True           # reintenta si hay timeout
            )
            # Verificar conexión inicial
            _redis_client.ping()
            logger.info("[Redis] Conexión establecida correctamente")
        except redis.ConnectionError as e:
            logger.error(f"[Redis] Error de conexión: {e}")
            raise
        except Exception as e:
            logger.error(f"[Redis] Error inesperado: {e}")
            raise
    return _redis_client

def close_redis_connection() -> bool:
    """
    Cierra la conexión global con Redis.
    :return: True si se cerró correctamente, False si hubo error
    """
    global _redis_client
    if _redis_client:
        try:
            _redis_client.close()
            logger.info("[Redis] Conexión cerrada")
            _redis_client = None
            return True
        except Exception as e:
            logger.error(f"[Redis] Error al cerrar conexión: {e}")
            return False
    return True

def test_redis_connection() -> bool:
    """
    Verifica si Redis está accesible.
    :return: True si responde al ping, False si no
    """
    try:
        client = get_redis_client()
        client.ping()
        logger.debug("[Redis] Ping exitoso")
        return True
    except Exception as e:
        logger.error(f"[Redis] Ping fallido: {e}")
        return False

def flush_redis() -> bool:
    """
    Limpia toda la base de datos Redis.
    :return: True si se limpió correctamente, False si hubo error
    """
    try:
        client = get_redis_client()
        client.flushdb()
        logger.warning("[Redis] Caché completo limpiado")
        return True
    except Exception as e:
        logger.error(f"[Redis] Error al limpiar Redis: {e}")
        return False
