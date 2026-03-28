# backend/app/utils/logger.py
"""
Logger
------
Configuración centralizada de logs para N.O.V.A.
- Crea automáticamente la carpeta de logs
- Maneja rotación de archivos para evitar crecimiento infinito
- Configuración consistente para consola y archivo
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configuración de handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    "logs/nova.log",
    maxBytes=5 * 1024 * 1024,   # 5 MB por archivo
    backupCount=5,              # mantiene 5 archivos de respaldo
    encoding="utf-8"
)

# Formato premium
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Configuración básica
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)

# Instancia global
logger = logging.getLogger("NOVA")

def get_logger(name: str) -> logging.Logger:
    """
    Devuelve un logger con nombre específico.
    """
    return logging.getLogger(name)
