"""
Modelo de Chat Premium
----------------------
Historial de conversaciones de N.O.V.A con trazabilidad empresarial.
Incluye métricas avanzadas, seguridad y control total.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, func
from sqlalchemy.orm import relationship
from app.db.postgresql import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)

    session_id = Column(String(100), nullable=True)            # Sesión única
    ip_address = Column(String(45), nullable=True)             # IP del usuario
    agent_type = Column(String(50), default="student")         # Tipo de agente

    message = Column(String(2000), nullable=False)             # Mensaje del usuario
    response = Column(String(4000), nullable=True)             # Respuesta del agente
    status = Column(String(50), default="sent")                # sent, read, error
    content_type = Column(String(50), default="text")          # text, image, file
    language = Column(String(10), default="es")                # Idioma detectado

    tokens_used = Column(Integer, default=0)                   # Tokens consumidos
    latency_ms = Column(Integer, default=0)                    # Tiempo de respuesta
    confidence_score = Column(Float, default=0.0)              # Confianza de la IA

    archived = Column(Boolean, default=False)                  # Archivado
    important = Column(Boolean, default=False)                 # Marcado como importante

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="chats")
    agent = relationship("Agent")

    def __repr__(self) -> str:
        return (
            f"<Chat id={self.id} user={self.user_id} "
            f"agent={self.agent_id} status={self.status} tokens={self.tokens_used}>"
        )

    def to_dict(self) -> dict:
        """
        Convierte el objeto Chat en un diccionario enriquecido.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "agent_type": self.agent_type,
            "message": self.message,
            "response": self.response,
            "status": self.status,
            "content_type": self.content_type,
            "language": self.language,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "confidence_score": self.confidence_score,
            "archived": self.archived,
            "important": self.important,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    # --- Métodos premium ---
    def mark_as_error(self, error_message: str | None = None) -> None:
        self.status = "error"
        if error_message:
            self.response = error_message

    def mark_as_read(self) -> None:
        self.status = "read"

    def mark_as_sent(self) -> None:
        self.status = "sent"

    def increment_tokens(self, amount: int) -> None:
        self.tokens_used += amount

    def set_latency(self, ms: int) -> None:
        self.latency_ms = ms

    def set_confidence(self, score: float) -> None:
        self.confidence_score = score

    def archive(self) -> None:
        self.archived = True

    def mark_as_important(self) -> None:
        self.important = True
