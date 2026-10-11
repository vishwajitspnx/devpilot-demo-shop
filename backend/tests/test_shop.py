from fastapi.testclient import TestClient

from app import pricing
from app.main import app

client = TestClient(app)


def test_subtotal_and_tax():
    result = pricing.total([(1000, 2), (250, 1)], tax_rate=0.1)
    assert result == {"subtotal": 2250, "discount": 0, "tax": 225, "total": 2475}


def test_discount_code_is_case_insensitive():
    assert pricing.total([(1000, 1)], 0.0, " welcome10 ")["discount"] == 100


def test_unknown_discount_code_gives_nothing():
    assert pricing.total([(1000, 1)], 0.0, "FREE")["discount"] == 0


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_products_and_cart():
    products = client.get("/api/products").json()
    assert len(products) >= 3
    r = client.post("/api/cart/total", json={"items": [{"product_id": products[0]["id"], "quantity": 2}]})
    assert r.status_code == 200 and r.json()["total"] > 0


def test_unknown_product_is_404():
    r = client.post("/api/cart/total", json={"items": [{"product_id": "nope", "quantity": 1}]})
    assert r.status_code == 404


def test_web_page_is_served():
    assert "Demo Shop" in client.get("/").text
