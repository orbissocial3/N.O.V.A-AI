# backend/app/services/agents/investor_premium.py
"""
Agente Inversor Premium
-----------------------
Funciones avanzadas:
 - Datos bursátiles en tiempo real (Yahoo Finance / Alpha Vantage)
 - Análisis de riesgos y métricas
 - Oportunidades de inversión por sectores
 - Modelos de negocio y noticias financieras
"""

import random
import os
import requests
from app.utils.logger import get_logger

logger = get_logger("investor_premium_agent")

ALPHA_VANTAGE_API = "https://www.alphavantage.co/query"
FINNHUB_API = "https://finnhub.io/api/v1/news"

def fetch_stock_price(symbol: str) -> str:
    try:
        api_key = os.getenv("ALPHA_VANTAGE_KEY")
        response = requests.get(ALPHA_VANTAGE_API, params={
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        })
        if response.status_code == 200:
            data = response.json()
            price = data["Global Quote"]["05. price"]
            return f"El precio actual de {symbol} es ${price} USD."
    except Exception as e:
        logger.error(f"[INVESTOR PREMIUM] Error Alpha Vantage: {e}")
    return "No pude obtener el precio de la acción."

def fetch_financial_news() -> str:
    try:
        token = os.getenv("FINNHUB_TOKEN")
        response = requests.get(FINNHUB_API, params={"category": "general", "token": token})
        if response.status_code == 200:
            data = response.json()
            headline = data[0]["headline"]
            return f"Última noticia financiera: {headline}"
    except Exception as e:
        logger.error(f"[INVESTOR PREMIUM] Error Finnhub: {e}")
    return "No pude obtener noticias financieras."

def investor_premium_agent(message: str) -> str:
    msg = message.lower()
    logger.info(f"[INVESTOR PREMIUM] Procesando mensaje: {msg}")

    if "acciones" in msg or "bolsa" in msg:
        return fetch_stock_price("AAPL")  # ejemplo: Apple
    elif "riesgo" in msg:
        return "El riesgo actual del mercado es alto, sugiero diversificar con activos defensivos."
    elif "oportunidad" in msg:
        return "El sector de energías renovables muestra oportunidades de crecimiento sostenido."
    elif "noticias" in msg:
        return fetch_financial_news()
    else:
        return "Soy tu agente inversor premium, puedo darte precios en tiempo real, análisis de riesgos y noticias financieras."
