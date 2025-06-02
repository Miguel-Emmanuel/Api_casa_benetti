from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from sqlalchemy import text

client = TestClient(app)

def setup_function():
    # Limpia la tabla de usuarios antes de cada test
    db = SessionLocal()
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()

def test_create_user():
    response = client.post("/users/", json={"email": "test@test.com", "password": "secret"})
    assert response.status_code == 200
