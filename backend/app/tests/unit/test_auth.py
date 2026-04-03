"""
Unit Test - Auth
----------------
Pruebas unitarias para autenticación de usuarios.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_with_valid_credentials():
    response = client.post("/auth/login", json={"email": "test@nova.ai", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_invalid_credentials():
    response = client.post("/auth/login", json={"email": "wrong@nova.ai", "password": "badpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"
