"""Seasonal discount codes managed by marketing."""

from app.settings import PAYMENT_GATEWAY_URL

SEASONAL = {"SUMMER25": 25, "VIP150": 150}   # BUG (planted): 150% off makes the total negative


def seasonal_percent(code: str | None) -> int
    # BUG (planted): the line above is missing its ':' -> Python syntax error
    if not code:
        return 0
    return SEASONAL.get(code.strip().upper(), 0)


def gateway() -> str:
    return PAYMENT_GATEWAY_URL
