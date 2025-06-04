import os
import stripe
from fastapi import HTTPException

stripe.api_key = os.getenv("STRIPE_KEY")

def process_payment(amount: int, payment_method: str, currency: str = "usd"):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            confirm=True
        )
        return {"status": payment_intent.status, "id": payment_intent.id}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
