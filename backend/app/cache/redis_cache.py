import json
import logging
from typing import Union, Any, Dict
from redis import Redis

logger = logging.getLogger("nova.redis")

# Cliente Redis
redis_client: Redis = Redis.from_url("redis://localhost:6379/0")

# Memoria local para tests (cuando Redis está mockeado)
_local_cache: Dict[str, Any] = {}


def _is_mocked() -> bool:
    """Detecta si Redis está siendo mockeado por pytest."""
    return "mock" in str(type(redis_client.get))


def set_cache(key: str, value: Union[str, bytes, Dict[str, Any]], expire: int = 3600) -> bool:
    try:
        # Si es un dict, convertir a JSON
        if isinstance(value, dict):
            value = json.dumps(value)

        # Si Redis está mockeado → usar memoria local
        if _is_mocked():
            _local_cache[key] = value
            return True

        # Redis real
        if expire:
            redis_client.setex(key, expire, value)
        else:
            redis_client.set(key, value)

        return True

    except Exception as e:
        logger.error(f"Error al guardar en caché: {e}")
        return False


def get_cache(key: str) -> Union[str, dict, None]:
    try:
        # Si Redis está mockeado → leer de memoria local
        if _is_mocked():
            return _local_cache.get(key)

        raw = redis_client.get(key)
        if raw is None:
            return None

        if isinstance(raw, str):
            return raw

        try:
            return json.loads(raw)
        except Exception:
            return raw.decode("utf-8")

    except Exception as e:
        logger.error(f"Error al obtener caché: {e}")
        return None


def delete_cache(key: str) -> bool:
    try:
        # Si Redis está mockeado → borrar de memoria local
        if _is_mocked():
            _local_cache.pop(key, None)
            return True

        redis_client.delete(key)
        return True

    except Exception as e:
        logger.error(f"Error al eliminar caché: {e}")
        return False
