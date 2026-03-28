# backend/app/routes/admin.py
"""
Rutas de Administración
-----------------------
Acceso restringido para métricas, logs y gestión avanzada.
Incluye validación estricta, auditoría, métricas, trazabilidad y seguridad.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.postgresql import get_db
from app.models.user import User
from app.utils.logger import get_logger
from app.utils.security import get_current_user
from app.monitoring import metrics, tracing, alerts

import time

logger = get_logger("admin")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "No encontrado"}}
)

# --- Modelos de respuesta ---
class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True

# --- Helper ---
def admin_required(user: User):
    """Verifica que el usuario tenga rol de administrador."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores"
        )
    return True

# --- Endpoints ---
@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todos los usuarios registrados.
    Solo accesible por administradores.
    """
    admin_required(current_user)
    start = time.time()
    try:
        with tracing.start_span("admin:list_users"):
            users = db.query(User).all()
            logger.info(f"[ADMIN] Listado de usuarios solicitado | total={len(users)} by={current_user.email}")
            metrics.record_request("GET", "/admin/users")
            metrics.record_latency("/admin/users", time.time() - start)
            return users
    except Exception as e:
        metrics.record_error("/admin/users")
        alerts.send_alert(f"Error al listar usuarios: {e}", severity="CRITICAL")
        logger.error(f"[ADMIN] Error al listar usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar usuarios")

@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Elimina un usuario por ID.
    Solo accesible por administradores.
    """
    admin_required(current_user)
    start = time.time()
    try:
        with tracing.start_span("admin:delete_user"):
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            db.delete(user)
            db.commit()
            logger.warning(f"[ADMIN] Usuario eliminado | id={user_id} by={current_user.email}")
            metrics.record_request("DELETE", "/admin/user/{user_id}")
            metrics.record_latency("/admin/user/{user_id}", time.time() - start)
            return {"message": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        metrics.record_error("/admin/user/{user_id}")
        alerts.send_alert(f"Error al eliminar usuario {user_id}: {e}", severity="CRITICAL")
        logger.error(f"[ADMIN] Error al eliminar usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar usuario")
