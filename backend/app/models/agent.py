# backend/app/models/agents.py
"""
Modelo de Agente IA
-------------------
Define los agentes disponibles en la plataforma N.O.V.A:
Ejemplos: Estudiante, Programador, Secretario, Inversor, Creativo.
Incluye metadatos, control de versiones y trazabilidad.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)       # Ej: Estudiante, Programador
    description = Column(String(255), nullable=False)            # Breve descripción del agente
    category = Column(String(50), nullable=False)                # Ej: Educativo, Finanzas, Creatividad
    version = Column(String(20), default="1.0")                  # Versión del agente
    is_premium = Column(Boolean, default=False)                  # True si requiere plan Premium/Empresarial

    # Metadatos premium
    created_at = Column(DateTime(timezone=True), server_default=func.now())   # Fecha de creación
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())         # Última actualización
    is_active = Column(Boolean, default=True)                                 # Control de activación

    def __repr__(self) -> str:
        return (
            f"<Agent id={self.id} name={self.name} "
            f"category={self.category} premium={self.is_premium}>"
        )

    def to_dict(self) -> dict:
        """
        Convierte el modelo en un diccionario (útil para APIs).
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "is_premium": self.is_premium,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def activate(self) -> None:
        """Activa el agente."""
        self.is_active = True

    def deactivate(self) -> None:
        """Desactiva el agente."""
        self.is_active = False

    def upgrade_version(self, new_version: str) -> None:
        """Actualiza la versión del agente."""
        self.version = new_version
