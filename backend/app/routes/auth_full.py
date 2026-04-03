# backend/app/routes/auth_full.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from app.db.postgresql import get_db
from app.models.user import User
from app.utils.logger import get_logger
from app.config import settings
from app.monitoring import alerts, metrics

router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger("auth")

# --- Configuración ---
load_dotenv(".env")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = settings.TOKEN_EXPIRATION_HOURS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Login con protección ---
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_remote_address(request)
    user: User | None = db.query(User).filter(User.email == data.email).first()

    if not user:
        logger.warning(f"[AUTH] Intento de login con email inexistente: {data.email} | ip={ip}")
        metrics.record_error("/auth/login", severity="WARNING")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    if not verify_password(data.password, user.hashed_password):
        logger.warning(f"[AUTH] Password incorrecto | user={data.email} | ip={ip}")
        metrics.record_error("/auth/login", severity="WARNING")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    logger.info(f"[AUTH] Login exitoso | user={user.email} | ip={ip}")
    metrics.record_request("POST", "/auth/login")

    return TokenResponse(access_token=access_token)

# --- Esqueleto para OAuth2 con Google ---
@router.get("/google/login")
def google_login():
    return {"detail": "Endpoint de inicio OAuth2 con Google (pendiente de implementación)"}

@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    return {"detail": "Callback de OAuth2 con Google (pendiente de implementación)"}
