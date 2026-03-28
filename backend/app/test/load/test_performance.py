"""
Load Test - Performance
-----------------------
Pruebas de rendimiento para endpoints críticos.
"""

import time
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint_performance():
    start = time.time()
    response = client.post("/chat/", json={"user_id": 1, "agent_id": 1, "message": "Hola"})
    duration = time.time() - start
    assert response.status_code == 200
    assert duration < 1.0  # El endpoint debe responder en menos de 1 segundo
