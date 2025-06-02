from fastapi import FastAPI, Depends, HTTPException
from . import schemas, models, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Pagos Casa Benetti")

# Dependencia para obtener la sesión de base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Bienvenido al sistema de pagos"}

# 1. Registrar nuevos usuarios
@app.post("/users/", response_model=schemas.UserCreate, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db=db, user=user)

# 2. Iniciar una transacción de pago
@app.post("/transactions/", status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar autorización antes de crear
    if not authorize_payment(transaction.user_id, transaction.amount):
        raise HTTPException(status_code=400, detail="Transacción no autorizada")
    return crud.create_transaction(db=db, transaction=transaction)

# 3. Consultar historial de transacciones de un usuario
@app.get("/users/{user_id}/transactions/")
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = crud.get_user_transactions(db, user_id=user_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No hay transacciones")
    return transactions

# 4. Validar que una transacción esté autorizada antes de procesarla
from typing import Optional

def authorize_payment(user_id: int, amount: float) -> bool:
    # Lógica simulada de autorización (puedes mejorarla según tus reglas)
    return amount <= 1000

@app.post("/transactions/authorize/")
def authorize_transaction(transaction: schemas.TransactionCreate):
    if not authorize_payment(transaction.user_id, transaction.amount):
        raise HTTPException(status_code=400, detail="Transacción no autorizada")
    return {"detail": "Autorizada"}

# Ejemplo de uso de endpoints:
# - POST /users/ {"email": "nuevo@correo.com", "password": "clave"}
# - POST /transactions/ {"user_id": 1, "amount": 500, "status": "pending"}
# - GET /users/1/transactions/
# - POST /transactions/authorize/ {"user_id": 1, "amount": 500, "status": "pending"}
# Puedes probar todo en /docs
