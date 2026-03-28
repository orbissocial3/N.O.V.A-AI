"""
Unit Test - Redis Cache
-----------------------
Pruebas unitarias para set_cache, get_cache y delete_cache.
"""

import pytest
from app.cache.redis_cache import set_cache, get_cache, delete_cache

def test_set_and_get_cache():
    key = "test:key"
    value = "valor de prueba"

    # Guardar en caché
    set_cache(key, value, expire=5)

    # Recuperar desde caché
    cached_value = get_cache(key)
    assert cached_value == value

def test_delete_cache():
    key = "test:delete"
    value = "valor temporal"

    # Guardar en caché
    set_cache(key, value, expire=5)

    # Eliminar
    delete_cache(key)

    # Verificar que ya no existe
    cached_value = get_cache(key)
    assert cached_value is None
