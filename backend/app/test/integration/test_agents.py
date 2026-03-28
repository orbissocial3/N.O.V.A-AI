"""
Integration Test - Text Agents
------------------------------
Prueba de integración para agentes IA de texto.
"""

import pytest
from app.services.agents.student import student_agent
from app.services.agents.programmer import programmer_agent

def test_student_agent_response():
    message = "Explica la fotosíntesis"
    response = student_agent(message)
    assert isinstance(response, str)
    assert "clorofila" in response.lower()

def test_programmer_agent_response():
    message = "Escribe un bucle en Python"
    response = programmer_agent(message)
    assert isinstance(response, str)
    assert "for" in response.lower() or "while" in response.lower()
