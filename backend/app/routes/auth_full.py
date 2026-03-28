# backend/app/routes/auth_full.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.postgresql import get_db
from app.models.user import User
from app.utils.logger import get_logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

logger = get_logger("auth")

# Configuración JWT
SECRET_KEY = "CAMBIA_ESTO_POR_UNA_CLAVE_SECRETA_LARGA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting (anti fuerza bruta)
limiter = Limiter(key_func=get_remote_address)

# --- Modelos ---
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Utilidades ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Login con protección ---
@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")  # máximo 5 intentos por minuto por IP
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """
    Login real con email + password contra PostgreSQL.
    Valida con bcrypt y devuelve JWT.
    Protegido contra fuerza bruta con rate limiting.
    """

    user: User | None = db.query(User).filter(User.email == data.email).first()
    if not user:
        logger.warning(f"[AUTH] Intento de login con email inexistente: {data.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    if not verify_password(data.password, user.hashed_password):
        logger.warning(f"[AUTH] Password incorrecto para usuario: {data.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    logger.info(f"[AUTH] Login exitoso | user={user.email}")

    return TokenResponse(access_token=access_token)

# --- Esqueleto para OAuth2 con Google ---
@router.get("/google/login")
def google_login():
    """
    Punto de entrada para OAuth2 con Google.
    Aquí normalmente rediriges al endpoint de autorización de Google.
    """
    return {"detail": "Endpoint de inicio OAuth2 con Google (pendiente de implementación)"}

@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Callback de Google OAuth2.
    Aquí intercambias 'code' por tokens de Google, obtienes el perfil,
    creas/actualizas el usuario en PostgreSQL y emites tu propio JWT.
    """
    # TODO: implementar integración real con Google
    return {"detail": "Callback de OAuth2 con Google (pendiente de implementación)"}
