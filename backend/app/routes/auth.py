from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    if data.email == "test@nova.ai" and data.password == "password123":
        return {"access_token": "fake-token", "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Credenciales inválidas")
