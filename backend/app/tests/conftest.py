# backend/app/test/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    # Creamos un cliente falso
    fake_redis = MagicMock()
    fake_redis.set = MagicMock(return_value=True)
    fake_redis.get = MagicMock(return_value="mocked_value")
    fake_redis.hset = MagicMock(return_value=1)
    fake_redis.hgetall = AsyncMock(return_value={"key": "value"})
    fake_redis.flushdb = MagicMock(return_value=True)

    # Sustituimos la función que devuelve el cliente real
    monkeypatch.setattr("app.cache.redis_cache.redis_client", fake_redis)

    return fake_redis
