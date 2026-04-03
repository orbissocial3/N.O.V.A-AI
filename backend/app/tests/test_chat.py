"""
Test de Chat Premium
--------------------
Valida que los agentes IA responden y que los chats se guardan en DB.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.postgresql import get_db
from sqlalchemy.orm import Session
from app.models.chat import Chat

client = TestClient(app)

# --- Fixtures ---
@pytest.fixture
def db_session() -> Session:
    # Usa la sesión real de tu DB de pruebas
    return next(get_db())

# --- Tests ---
def test_create_chat_student(db_session):
    """
    Valida que el agente estudiante responde y guarda el chat.
    """
    response = client.post(
        "/chat/",
        params={"user_id": 1, "agent_id": 1, "message": "Hola, necesito ayuda con matemáticas"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == 1
    assert "response" in data
    assert data["status"] == "sent"

    # Verificar que se guardó en DB
    chat = db_session.query(Chat).filter(Chat.id == data["id"]).first()
    assert chat is not None
    assert chat.message == "Hola, necesito ayuda con matemáticas"

def test_create_chat_programmer(db_session):
    """
    Valida que el agente programador responde.
    """
    response = client.post(
        "/chat/",
        params={"user_id": 1, "agent_id": 2, "message": "Escribe un script en Python"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == 2
    assert "response" in data

def test_create_chat_invalid_agent():
    """
    Valida que un agente no reconocido devuelve error.
    """
    response = client.post(
        "/chat/",
        params={"user_id": 1, "agent_id": 99, "message": "Prueba con agente inexistente"}
    )
    assert response.status_code == 400 or "error" in response.json()
