# backend/app/config.py
"""
Configuración global de N.O.V.A
--------------------------------
Centraliza todas las variables de entorno y parámetros:
- Seguridad
- Bases de datos
- Pagos
- Logs
- Correo electrónico
- Almacenamiento
- APIs externas
- Internacionalización
"""

import os
from typing import List
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- General ---
    APP_NAME: str = Field(default="N.O.V.A AI App")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default=os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development") == "development")
    PORT: int = Field(default=int(os.getenv("PORT", 8000)))

    # --- Seguridad ---
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "supersecretkey123"))
    JWT_SECRET: str = Field(default=os.getenv("JWT_SECRET", "jwtsecretkey"))
    TOKEN_EXPIRATION_HOURS: int = Field(default=96)
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_ALLOWED_ORIGINS: str = Field(default=os.getenv("CORS_ALLOWED_ORIGINS", ""))

    # --- Bases de datos ---
    POSTGRES_URL: str = Field(default=os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/nova_db"))
    DB_URL: str = POSTGRES_URL
    MONGO_URL: str = Field(default=os.getenv("MONGO_URL", "mongodb://localhost:27017/nova_db"))
    REDIS_URL: str = Field(default=os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    REDIS_HOST: str = REDIS_URL
    CASSANDRA_HOSTS: List[str] = ["127.0.0.1"]

    # --- Métodos de pago ---
    PAYPAL_CLIENT_ID: str = Field(default=os.getenv("PAYPAL_CLIENT_ID", ""))
    PAYPAL_SECRET: str = Field(default=os.getenv("PAYPAL_SECRET", ""))
    STRIPE_API_KEY: str = Field(default=os.getenv("STRIPE_API_KEY", ""))
    GOOGLE_PLAY_KEY: str = Field(default=os.getenv("GOOGLE_PLAY_KEY", ""))

    # --- Logs ---
    LOG_LEVEL: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))
    LOG_FILE: str = Field(default=os.getenv("LOG_FILE", "logs/nova.log"))

    # --- Correo electrónico ---
    SMTP_SERVER: str = Field(default=os.getenv("SMTP_SERVER", "smtp.gmail.com"))
    SMTP_PORT: int = Field(default=int(os.getenv("SMTP_PORT", 587)))
    SMTP_USER: str = Field(default=os.getenv("SMTP_USER", ""))
    SMTP_PASSWORD: str = Field(default=os.getenv("SMTP_PASSWORD", ""))
    SENDGRID_API_KEY: str = Field(default=os.getenv("SENDGRID_API_KEY", ""))

    # --- Almacenamiento ---
    STORAGE_PROVIDER: str = Field(default=os.getenv("STORAGE_PROVIDER", "local"))
    STORAGE_PATH: str = Field(default=os.getenv("STORAGE_PATH", "storage/"))
    S3_BUCKET: str = Field(default=os.getenv("S3_BUCKET", ""))
    S3_ACCESS_KEY: str = Field(default=os.getenv("S3_ACCESS_KEY", ""))
    S3_SECRET_KEY: str = Field(default=os.getenv("S3_SECRET_KEY", ""))

    # --- APIs externas ---
    OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    ANTHROPIC_API_KEY: str = Field(default=os.getenv("ANTHROPIC_API_KEY", ""))
    GOOGLE_AI_API_KEY: str = Field(default=os.getenv("GOOGLE_AI_API_KEY", ""))
    NEWS_API_KEY: str = Field(default=os.getenv("NEWS_API_KEY", ""))
    GOOGLE_SEARCH_API_KEY: str = Field(default=os.getenv("GOOGLE_SEARCH_API_KEY", ""))
    GOOGLE_SEARCH_ENGINE_ID: str = Field(default=os.getenv("GOOGLE_SEARCH_ENGINE_ID", ""))
    WIKIMEDIA_API_URL: str = Field(default=os.getenv("WIKIMEDIA_API_URL", "https://en.wikipedia.org/w/api.php"))
    YOUTUBE_API_KEY: str = Field(default=os.getenv("YOUTUBE_API_KEY", ""))
    TWITTER_BEARER_TOKEN: str = Field(default=os.getenv("TWITTER_BEARER_TOKEN", ""))
    GITHUB_API_TOKEN: str = Field(default=os.getenv("GITHUB_API_TOKEN", ""))
    STACKEXCHANGE_API_KEY: str = Field(default=os.getenv("STACKEXCHANGE_API_KEY", ""))

    # --- Internacionalización ---
    SUPPORTED_LANGUAGES: List[str] = ["es", "en", "fr"]

    # --- Empresarial ---
    ENABLE_2FA: bool = True
    MAX_REQUESTS_FREE: int = 1000
    MAX_REQUESTS_PREMIUM: int = 10000
    MAX_REQUESTS_ENTERPRISE: int = 50000

    # --- Configuración Pydantic v2 ---
    model_config = ConfigDict(env_file=".env", case_sensitive=True)

    # --- Validadores ---
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        if v not in ["development", "staging", "production"]:
            raise ValueError("ENVIRONMENT debe ser development, staging o production")
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v or len(v) < 12:
            raise ValueError("SECRET_KEY debe tener al menos 12 caracteres")
        return v

# Instancia global
settings = Settings()
