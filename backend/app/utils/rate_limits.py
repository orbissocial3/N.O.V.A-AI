# backend/app/utils/rate_limits.py
"""
Rate Limits
-----------
Control de uso por plan (Free, Premium, Empresarial).
"""
from app.config import settings
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.plan import Plan

def check_rate_limit(user_id: int, db: Session):
    """
    Verifica si el usuario ha excedido el límite de peticiones según su plan.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.plan:
        raise HTTPException(status_code=403, detail="Usuario sin plan activo")

    plan = user.plan
    # Definir límites
    limits = {
        "Free": settings.MAX_REQUESTS_FREE,
        "Premium": settings.MAX_REQUESTS_PREMIUM,
        "Empresarial": settings.MAX_REQUESTS_ENTERPRISE
    }

    max_requests = limits.get(plan.name, settings.MAX_REQUESTS_FREE)

    # Aquí deberías tener un contador de requests (ej. Redis o DB)
    # Simulación: si el usuario tiene más de X chats, bloquear
    chat_count = len(user.chats)
    if chat_count >= max_requests:
        raise HTTPException(status_code=429, detail="Límite de uso alcanzado")

    return True
def check_rate_limit(user_id: str) -> bool:
    # TODO: implementar lógica real con Redis/DB
    return True
