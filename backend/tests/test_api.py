"""
Phase 4 tests: run with `pytest -v tests/test_api.py`

Uses FastAPI's TestClient. Implement `app/main.py` (and the earlier
phases it depends on) until these pass.

Note: `store` is a module-level singleton in `app.main`, so each test
adds to the same in-memory store - tests are written to account for that.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_bag():
    response = client.post(
        "/bags",
        json={
            "id": "api-1",
            "brand": "Chanel",
            "model": "Classic Flap Medium",
            "color": "Black",
            "condition": "like_new",
            "source": "test",
            "price": 9500.0,
            "currency": "USD",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == "api-1"
    assert body["current_price"]["price"] == 9500.0

    get_response = client.get("/bags/api-1")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == "api-1"


def test_get_missing_bag_returns_404():
    response = client.get("/bags/does-not-exist")
    assert response.status_code == 404


def test_list_bags_includes_created():
    client.post(
        "/bags",
        json={
            "id": "api-2",
            "brand": "Louis Vuitton",
            "model": "Neverfull MM",
            "color": "Monogram",
            "condition": "gently_used",
            "source": "test",
            "price": 1450.0,
            "currency": "USD",
        },
    )

    response = client.get("/bags")
    assert response.status_code == 200
    ids = {b["id"] for b in response.json()}
    assert "api-2" in ids


def test_cheapest_endpoint():
    client.post(
        "/bags",
        json={
            "id": "api-cheap",
            "brand": "Coach",
            "model": "Tabby 26",
            "color": "Brown",
            "condition": "new",
            "source": "test",
            "price": 350.0,
            "currency": "USD",
        },
    )

    response = client.get("/bags/cheapest?n=1")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == "api-cheap"
