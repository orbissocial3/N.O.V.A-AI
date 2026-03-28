# backend/app/models/chat.py
"""
Modelo de Chat
--------------
Define el historial de conversaciones de cada usuario en N.O.V.A.
Incluye mensajes, agente utilizado, estado, métricas de uso y trazabilidad.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.postgresql import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)

    message = Column(String(2000), nullable=False)             # Mensaje del usuario
    response = Column(String(4000), nullable=True)             # Respuesta del agente
    status = Column(String(50), default="sent")                # sent, read, error
    content_type = Column(String(50), default="text")          # text, image, file
    language = Column(String(10), default="es")                # Idioma detectado
    tokens_used = Column(Integer, default=0)                   # Tokens consumidos

    # Timestamps premium
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="chats")
    agent = relationship("Agent")

    def __repr__(self) -> str:
        return (
            f"<Chat id={self.id} user={self.user_id} "
            f"agent={self.agent_id} status={self.status}>"
        )

    def to_dict(self) -> dict:
        """
        Convierte el objeto Chat en un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "message": self.message,
            "response": self.response,
            "status": self.status,
            "content_type": self.content_type,
            "language": self.language,
            "tokens_used": self.tokens_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def mark_as_error(self, error_message: str | None = None) -> None:
        """
        Marca el chat como error y opcionalmente guarda un mensaje de error.
        """
        self.status = "error"
        if error_message:
            self.response = error_message

    def mark_as_read(self) -> None:
        """
        Marca el chat como leído.
        """
        self.status = "read"

    def mark_as_sent(self) -> None:
        """
        Marca el chat como enviado.
        """
        self.status = "sent"

    def increment_tokens(self, amount: int) -> None:
        """
        Incrementa el contador de tokens usados.
        """
        self.tokens_used += amount
