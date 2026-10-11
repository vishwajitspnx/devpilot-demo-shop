"""Demo Shop: a tiny online shop (API + web page) used to try out DevPilot."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import pricing

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
VERSION = "1.0.0"

app = FastAPI(title="Demo Shop", version=VERSION)


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SETTINGS = load_json("settings.json")
PRODUCTS = {p["id"]: p for p in load_json("products.json")}


class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, le=99)


class Cart(BaseModel):
    items: list[CartItem] = Field(min_length=1)
    discount_code: str | None = None


@app.get("/health")
def health() -> dict:
    """Used by DevPilot (and any load balancer) to see if the shop is alive."""
    # BUG (planted): "maintenance_mode" is not in settings.json, so every health check crashes (HTTP 500)
    if SETTINGS["maintenance_mode"]:
        return {"status": "maintenance", "version": VERSION}
    return {"status": "ok", "version": VERSION, "store": SETTINGS["store_name"]}


@app.get("/api/products")
def products() -> list[dict]:
    return list(PRODUCTS.values())


@app.post("/api/cart/total")
def cart_total(cart: Cart) -> dict:
    lines = []
    for item in cart.items:
        product = PRODUCTS.get(item.product_id)
        if product is None:
            raise HTTPException(404, f"Unknown product {item.product_id}")
        lines.append((product["price"], item.quantity))
    return pricing.total(lines, SETTINGS["tax_rate"], cart.discount_code)


app.mount("/", StaticFiles(directory=ROOT / "ui", html=True), name="ui")
