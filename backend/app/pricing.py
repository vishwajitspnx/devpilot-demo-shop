"""Prices are in cents (integers) so totals never have rounding surprises."""

from __future__ import annotations

DISCOUNTS = {"WELCOME10": 10}   # code -> percent off


def subtotal(lines: list[tuple[int, int]]) -> int:
    return sum(price * quantity for price, quantity in lines)


def discount_percent(code: str | None) -> int:
    if not code:
        return 0
    return DISCOUNTS.get(code.strip().upper(), 0)


def total(lines: list[tuple[int, int]], tax_rate: float, code: str | None = None) -> dict:
    sub = subtotal(lines)
    off = sub * discount_percent(code) // 100
    tax = round((sub - off) * tax_rate)
    return {"subtotal": sub, "discount": off, "tax": tax, "total": sub - off + tax}
