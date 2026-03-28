# backend/app/services/payments.py
"""
Servicio de Pagos
-----------------
Implementa la lógica de integración con PayPal, Stripe y Google Play Billing.
Incluye creación de órdenes, validación de pagos y registro en la base de datos.
"""

import requests
import stripe
from sqlalchemy.orm import Session
from app.config import settings
from app.models.plan import Plan
from app.models.user import User
from app.utils.logger import get_logger

logger = get_logger("payments")

# --- Configuración de Stripe ---
stripe.api_key = settings.STRIPE_API_KEY

# --- PayPal ---
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Cambiar a live en producción

def create_paypal_order(amount: float, currency: str = "USD") -> dict:
    """
    Crear una orden de pago en PayPal.
    """
    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_SECRET}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"[PAYPAL] Orden creada | amount={amount} currency={currency}")
        return response.json()
    except Exception as e:
        logger.error(f"[PAYPAL] Error creando orden: {e}")
        return {"error": str(e)}

def capture_paypal_order(order_id: str) -> dict:
    """
    Capturar un pago de PayPal.
    """
    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_SECRET}"
    }
    try:
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"[PAYPAL] Pago capturado | order_id={order_id}")
        return response.json()
    except Exception as e:
        logger.error(f"[PAYPAL] Error capturando pago: {e}")
        return {"error": str(e)}

# --- Stripe ---
def create_stripe_payment(amount: float, currency: str = "usd") -> dict:
    """
    Crear un PaymentIntent en Stripe.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe usa centavos
            currency=currency,
            payment_method_types=["card"]
        )
        logger.info(f"[STRIPE] PaymentIntent creado | amount={amount} currency={currency}")
        return {"client_secret": intent.client_secret}
    except Exception as e:
        logger.error(f"[STRIPE] Error creando PaymentIntent: {e}")
        return {"error": str(e)}

# --- Google Play Billing ---
def validate_google_play_purchase(purchase_token: str) -> dict:
    """
    Validar una compra de Google Play Billing.
    """
    # Aquí normalmente se usaría la API de Google Play Developer
    # Simulación de validación
    if purchase_token.startswith("VALID"):
        logger.info(f"[GOOGLE PLAY] Compra validada | token={purchase_token}")
        return {"status": "success", "details": "Compra validada en Google Play"}
    logger.warning(f"[GOOGLE PLAY] Token inválido | token={purchase_token}")
    return {"status": "error", "details": "Token inválido"}

# --- Lógica empresarial ---
def assign_plan_to_user(user_id: int, plan_id: int, db: Session) -> dict:
    """
    Asignar un plan a un usuario después de un pago exitoso.
    """
    user = db.query(User).filter(User.id == user_id).first()
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not user or not plan:
        logger.error(f"[PAYMENTS] Usuario o plan no encontrado | user_id={user_id} plan_id={plan_id}")
        return {"error": "Usuario o plan no encontrado"}

    user.plan_id = plan.id
    db.commit()
    logger.info(f"[PAYMENTS] Plan asignado | user={user.email} plan={plan.name}")
    return {"message": f"Plan {plan.name} asignado a {user.email}"}
