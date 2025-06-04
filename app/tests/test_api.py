from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from sqlalchemy import text
import os
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    # Elimina la base de datos antes de cada test para asegurar un entorno limpio
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass  # Si está en uso, ignora (solo para evitar crash, pero no debería pasar)

def setup_function():
    db = SessionLocal()
    db.execute(text("DELETE FROM transactions"))
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()

def get_auth_headers(email, password):
    resp = client.post("/login/", data={"username": email, "password": password})
    assert resp.status_code == 200
    token = resp.json()["DATA"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_user():
    response = client.post("/users/", json={"email": "test1@correo.com", "password": "secret123"})
    assert response.status_code == 201
    data = response.json()["DATA"]
    assert data["email"] == "test1@correo.com"

def test_create_user_invalid_email():
    response = client.post("/users/", json={"email": "noesemail", "password": "secret123"})
    assert response.status_code == 422

def test_create_user_short_password():
    response = client.post("/users/", json={"email": "test2@correo.com", "password": "123"})
    assert response.status_code == 422 or response.status_code == 400

def test_create_duplicate_user():
    client.post("/users/", json={"email": "test3@correo.com", "password": "secret123"})
    response = client.post("/users/", json={"email": "test3@correo.com", "password": "secret123"})
    assert response.status_code == 400

def test_create_transaction():
    user_email = "trans@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    response = client.post("/transactions/", json={"user_id": user_id, "amount": 100, "status": "pending"}, headers=headers)
    assert response.status_code == 201

def test_create_transaction_negative_amount():
    user_email = "trans2@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    response = client.post("/transactions/", json={"user_id": user_id, "amount": -50, "status": "pending"}, headers=headers)
    assert response.status_code == 422 or response.status_code == 400

def test_create_transaction_invalid_status():
    user_email = "trans3@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    response = client.post("/transactions/", json={"user_id": user_id, "amount": 100, "status": "otro"}, headers=headers)
    assert response.status_code == 422 or response.status_code == 400

def test_get_user_transactions():
    user_email = "trans4@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    client.post("/transactions/", json={"user_id": user_id, "amount": 100, "status": "pending"}, headers=headers)
    response = client.get(f"/users/{user_id}/transactions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json()["DATA"], list)

def test_authorize_transaction():
    user_email = "trans5@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    response = client.post("/transactions/authorize/", json={"user_id": user_id, "amount": 500, "status": "pending"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["DATA"]["detail"] == "Autorizada"

def test_authorize_transaction_not_authorized():
    user_email = "trans6@correo.com"
    user_password = "secret123"
    user_resp = client.post("/users/", json={"email": user_email, "password": user_password})
    user_id = user_resp.json()["DATA"].get("id", 1)
    headers = get_auth_headers(user_email, user_password)
    response = client.post("/transactions/authorize/", json={"user_id": user_id, "amount": 2000, "status": "pending"}, headers=headers)
    assert response.status_code == 400
