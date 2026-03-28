# backend/app/db/postgresql.py
"""
PostgreSQL Connection
----------------------------
Gestión de conexión con PostgreSQL usando SQLAlchemy para N.O.V.A
- Engine con pool optimizado
- Sesiones seguras con manejo de errores
- Logging detallado
- Funciones utilitarias para inicializar y cerrar conexión
"""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings

logger = logging.getLogger("nova.postgresql")

# Crear engine con configuración premium
engine = create_engine(
    settings.POSTGRES_URL,     # Usamos POSTGRES_URL definido en config.py
    pool_pre_ping=True,        # Verifica conexión antes de usar
    pool_size=10,              # Tamaño del pool
    max_overflow=20,           # Conexiones extra permitidas
    pool_timeout=30,           # Tiempo máximo de espera
    echo=False                 # Cambiar a True para debug SQL
)

# Configurar SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False     # Evita invalidar objetos tras commit
)

def get_db() -> Generator[Session, None, None]:
    """
    Provee una sesión de base de datos.
    Uso recomendado: inyección de dependencias en FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"[PostgreSQL] Error en sesión: {e}")
        raise
    finally:
        db.close()
        logger.debug("[PostgreSQL] Sesión cerrada")

def init_db() -> bool:
    """
    Inicializa la conexión y verifica que la DB esté accesible.
    :return: True si la conexión fue exitosa, False si falló
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("[PostgreSQL] Conexión inicial verificada")
        return True
    except SQLAlchemyError as e:
        logger.error(f"[PostgreSQL] Error al inicializar DB: {e}")
        return False

def close_engine() -> bool:
    """
    Cierra el engine global (útil en tests o mantenimiento).
    :return: True si se cerró correctamente, False si hubo error
    """
    try:
        engine.dispose()
        logger.info("[PostgreSQL] Engine cerrado correctamente")
        return True
    except Exception as e:
        logger.error(f"[PostgreSQL] Error al cerrar engine: {e}")
        return False

def test_connection() -> bool:
    """
    Verifica si la base de datos responde.
    :return: True si responde, False si no
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.debug("[PostgreSQL] Ping exitoso")
        return True
    except Exception as e:
        logger.error(f"[PostgreSQL] Ping fallido: {e}")
        return False

from sqlalchemy.orm import declarative_base
Base = declarative_base()
