from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_hello_default():
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Hello, World!"


def test_hello_with_name():
    resp = client.get("/hello", params={"name": "Alice"})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Hello, Alice!"


def test_read_item():
    item_id = 42
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["item_id"] == item_id
    assert data["name"] == f"Item {item_id}"
    assert "description" in data