# backend/app/routes/admin.py
"""
Rutas de Administración
-----------------------
Acceso restringido para métricas, logs y gestión avanzada.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.postgresql import get_db
from app.models.user import User
from app.utils.logger import get_logger

logger = get_logger("admin")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "No encontrado"}}
)

def admin_required(user: User):
    """
    Verifica que el usuario tenga rol de administrador.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores"
        )
    return True

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    """
    Lista todos los usuarios registrados.
    """
    try:
        users = db.query(User).all()
        logger.info(f"[ADMIN] Listado de usuarios solicitado | total={len(users)}")
        return [user.to_dict() for user in users]
    except Exception as e:
        logger.error(f"[ADMIN] Error al listar usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar usuarios")

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario por ID.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(user)
        db.commit()
        logger.warning(f"[ADMIN] Usuario eliminado | id={user_id}")
        return {"message": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ADMIN] Error al eliminar usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al eliminar usuario")
