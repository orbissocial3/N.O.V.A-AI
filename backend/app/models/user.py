# backend/app/models/user.py
"""
Modelo de Usuario
-----------------
Define la estructura de los usuarios en la base de datos N.O.V.A.
Incluye información personal, plan activo, roles, seguridad y trazabilidad.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgresql import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)              # Email verificado
    role = Column(String(50), default="user")                 # user, admin
    two_factor_enabled = Column(Boolean, default=False)

    last_login = Column(DateTime(timezone=True), server_default=func.now())
    plan_id = Column(Integer, ForeignKey("plans.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    plan = relationship("Plan", back_populates="users")
    chats = relationship("Chat", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} email={self.email} "
            f"role={self.role} active={self.is_active}>"
        )

    def to_dict(self) -> dict:
        """
        Convierte el objeto User en un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role,
            "two_factor_enabled": self.two_factor_enabled,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "plan_id": self.plan_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    # Métodos de gestión premium
    def activate(self) -> None:
        """Activa el usuario."""
        self.is_active = True

    def deactivate(self) -> None:
        """Desactiva el usuario."""
        self.is_active = False

    def verify_email(self) -> None:
        """Marca el usuario como verificado."""
        self.is_verified = True

    def enable_two_factor(self) -> None:
        """Habilita la autenticación en dos pasos."""
        self.two_factor_enabled = True

    def disable_two_factor(self) -> None:
        """Deshabilita la autenticación en dos pasos."""
        self.two_factor_enabled = False

    def update_last_login(self) -> None:
        """Actualiza la fecha de último login."""
        from datetime import datetime
        self.last_login = datetime.utcnow()
