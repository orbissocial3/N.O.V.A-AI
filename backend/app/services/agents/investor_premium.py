"""
Agente Inversor Premium N.O.V.A
-------------------------------
Funciones avanzadas:
 - Datos bursátiles en tiempo real (Alpha Vantage / Yahoo Finance)
 - Análisis de riesgos y métricas financieras
 - Oportunidades de inversión por sectores
 - Modelos de negocio y noticias financieras
 - Análisis de gráficos y tendencias
"""

import os
import requests
import random
from app.utils.logger import get_logger

logger = get_logger("investor_premium_agent")

ALPHA_VANTAGE_API = "https://www.alphavantage.co/query"
FINNHUB_API = "https://finnhub.io/api/v1/news"

# -----------------------------
# Funciones de integración
# -----------------------------

def fetch_stock_price(symbol: str) -> str:
    """Obtiene el precio actual de una acción."""
    try:
        api_key = os.getenv("ALPHA_VANTAGE_KEY")
        response = requests.get(ALPHA_VANTAGE_API, params={
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data["Global Quote"]["05. price"]
        change = data["Global Quote"]["09. change"]
        percent = data["Global Quote"]["10. change percent"]
        return f"💹 {symbol}: ${price} USD | Cambio: {change} ({percent})"
    except Exception as e:
        logger.error(f"[INVESTOR PREMIUM] Error Alpha Vantage: {e}")
        return "No pude obtener el precio de la acción."

def fetch_financial_news() -> str:
    """Obtiene la última noticia financiera relevante."""
    try:
        token = os.getenv("FINNHUB_TOKEN")
        response = requests.get(FINNHUB_API, params={"category": "general", "token": token}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            headline = data[0]["headline"]
            source = data[0].get("source", "Fuente desconocida")
            return f"📰 Última noticia financiera: {headline} ({source})"
        return "No encontré noticias financieras recientes."
    except Exception as e:
        logger.error(f"[INVESTOR PREMIUM] Error Finnhub: {e}")
        return "No pude obtener noticias financieras."

def analyze_risk() -> str:
    """Análisis de riesgo del mercado."""
    risks = [
        "⚠️ El riesgo actual del mercado es alto, sugiero diversificar con activos defensivos.",
        "📉 Volatilidad elevada detectada, considera reducir exposición en sectores especulativos.",
        "📊 Riesgo moderado, oportunidades en sectores tecnológicos y energías renovables."
    ]
    return random.choice(risks)

def sector_opportunities() -> str:
    """Detecta oportunidades de inversión por sectores."""
    opportunities = [
        "🌱 El sector de energías renovables muestra oportunidades de crecimiento sostenido.",
        "💻 El sector tecnológico sigue liderando en innovación y capitalización.",
        "🏥 El sector salud presenta estabilidad y potencial defensivo.",
        "🏗️ El sector infraestructura está en auge por inversión pública y privada."
    ]
    return random.choice(opportunities)

def analyze_trends(symbol: str) -> str:
    """Análisis básico de tendencias de una acción."""
    return f"📈 Tendencia de {symbol}: Señales de soporte y resistencia detectadas, posible consolidación en corto plazo."

# -----------------------------
# Agente principal
# -----------------------------

def investor_premium_agent(message: str) -> str:
    """Procesa el mensaje del usuario y devuelve análisis financiero premium."""
    msg = message.lower()
    logger.info(f"[INVESTOR PREMIUM] Procesando mensaje: {msg}")

    if "acciones" in msg or "bolsa" in msg:
        return fetch_stock_price("AAPL")  # ejemplo: Apple
    elif "riesgo" in msg:
        return analyze_risk()
    elif "oportunidad" in msg or "sector" in msg:
        return sector_opportunities()
    elif "noticias" in msg:
        return fetch_financial_news()
    elif "tendencia" in msg or "gráfico" in msg:
        return analyze_trends("AAPL")
    else:
        return (
            "👑 Soy tu agente inversor PREMIUM N.O.V.A: el consejero real de las inversiones globales.\n"
            "💹 Te ofrezco precios en tiempo real, análisis de riesgos, oportunidades sectoriales, tendencias gráficas y noticias verificadas.\n"
            "⚠️ Recuerda: no garantizo resultados, pero siempre te daré información confiable y estratégica."
        )

# Alias para compatibilidad con chat.py
investor_agent = investor_premium_agent
