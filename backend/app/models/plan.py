# backend/app/models/plan.py
"""
Modelo de Plan
--------------
Define los planes de suscripción de N.O.V.A:
Free, Premium, Empresarial.
Incluye precios, duración, límites de uso y trazabilidad.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.postgresql import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)       # Free, Premium, Empresarial
    type = Column(String(50), nullable=False)                    # Tipo de plan
    price = Column(Float, nullable=False)                        # Precio en USD
    duration_days = Column(Integer, nullable=False)              # Ej: 7, 30, 90
    max_agents = Column(Integer, default=3)                      # Número de agentes disponibles
    max_storage_mb = Column(Integer, default=100)                # Límite de almacenamiento
    is_active = Column(Boolean, default=True)                    # Control de activación

    # Metadatos premium
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    users = relationship("User", back_populates="plan")

    def __repr__(self) -> str:
        return (
            f"<Plan id={self.id} name={self.name} "
            f"type={self.type} price={self.price} active={self.is_active}>"
        )

    def to_dict(self) -> dict:
        """
        Convierte el objeto Plan en un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "price": self.price,
            "duration_days": self.duration_days,
            "max_agents": self.max_agents,
            "max_storage_mb": self.max_storage_mb,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    # Métodos de gestión premium
    def activate(self) -> None:
        """Activa el plan."""
        self.is_active = True

    def deactivate(self) -> None:
        """Desactiva el plan."""
        self.is_active = False

    def upgrade_storage(self, extra_mb: int) -> None:
        """Incrementa el almacenamiento disponible del plan."""
        self.max_storage_mb += extra_mb

    def upgrade_agents(self, extra_agents: int) -> None:
        """Incrementa el número de agentes disponibles en el plan."""
        self.max_agents += extra_agents
