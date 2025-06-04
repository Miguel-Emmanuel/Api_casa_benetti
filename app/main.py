from fastapi import FastAPI, Depends, HTTPException, Request, Body, Query, Form
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from . import schemas, models, crud
from .database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from loguru import logger
import sys
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

load_dotenv()

Base.metadata.create_all(bind=engine)

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

# Helper para respuesta estándar
def standard_response(data, status: bool, code: int):
    return JSONResponse(content=jsonable_encoder({"DATA": data, "STATUS": status, "CODIGO": code}), status_code=code)

# 1. Registrar nuevos usuarios
@app.post("/users/", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return standard_response("Email ya registrado", False, 400)
    if len(user.password) < 6:
        return standard_response("La contraseña debe tener al menos 6 caracteres", False, 400)
    user_created = crud.create_user(db=db, user=user)
    user_data = schemas.UserResponse.model_validate(user_created).model_dump()
    return standard_response(user_data, True, 201)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

http_bearer = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(db, email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

# Inicializar rate limiter y logs
def is_test_env():
    return (
        bool(os.getenv("PYTEST_CURRENT_TEST")) or
        "pytest" in sys.modules
    )

IS_TEST = is_test_env()

if not IS_TEST:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar loguru para logs estructurados
logger.add("logs/api.log", rotation="1 week", retention="4 weeks", level="INFO")

class CustomLoginRequest(BaseModel):
    username: str
    password: str

@app.post("/custom-login/")
def custom_login(data: CustomLoginRequest, db: Session = Depends(get_db)):
    email = data.username
    password = data.password
    if not email or not password:
        return standard_response("Faltan username o password", False, 400)
    user = authenticate_user(db, email, password)
    if not user:
        return standard_response("Credenciales incorrectas", False, 401)
    # Generar client_id y client_secret en backend (ejemplo simple)
    client_id = f"cli_{user.id}"
    client_secret = f"sec_{user.id}"
    # Incluirlos en el token
    access_token = create_access_token(data={"sub": user.email, "client_id": client_id, "client_secret": client_secret}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(data={"sub": user.email, "type": "refresh", "client_id": client_id, "client_secret": client_secret}, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    return standard_response({"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}, True, 200)

@app.post("/login/")
def login(db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return standard_response("Faltan username o password", False, 400)
    user = authenticate_user(db, username, password)
    if not user:
        return standard_response("Credenciales incorrectas", False, 401)
    client_id = f"cli_{user.id}"
    client_secret = f"sec_{user.id}"
    access_token = create_access_token(data={"sub": user.email, "client_id": client_id, "client_secret": client_secret}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(data={"sub": user.email, "type": "refresh", "client_id": client_id, "client_secret": client_secret}, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    return standard_response({"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}, True, 200)

# Cambiar la seguridad de los endpoints protegidos a HTTPBearer
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# 2. Iniciar una transacción de pago
@app.post("/transactions/", status_code=201)
def create_transaction(
    transaction: schemas.TransactionCreate = Body(...),
    db: Session = Depends(get_db), 
    current_user: schemas.UserResponse = Depends(get_current_user)):
    user = crud.get_user(db, transaction.user_id)
    if not user:
        return standard_response("Usuario no encontrado", False, 404)
    if not authorize_payment(transaction.user_id, transaction.amount):
        return standard_response("Transacción no autorizada", False, 400)
    tx = crud.create_transaction(db=db, transaction=transaction)
    tx_data = schemas.TransactionResponse.model_validate(tx).model_dump()
    return standard_response(tx_data, True, 201)

# 3. Consultar historial de transacciones de un usuario
@app.get("/users/{user_id}/transactions/")
def get_user_transactions(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    transactions = crud.get_user_transactions(db, user_id=user_id)
    if not transactions:
        return standard_response("No hay transacciones", False, 404)
    txs = [schemas.TransactionResponse.model_validate(tx).model_dump() for tx in transactions]
    return standard_response(txs, True, 200)

# 4. Validar que una transacción esté autorizada antes de procesarla
from typing import Optional

def authorize_payment(user_id: int, amount: float) -> bool:
    # Lógica simulada de autorización (puedes mejorarla según tus reglas)
    return amount <= 1000

@app.post("/transactions/authorize/")
def authorize_transaction(transaction: schemas.TransactionCreate, current_user: schemas.UserResponse = Depends(get_current_user)):
    # Solo usuarios autenticados pueden validar transacciones
    if not authorize_payment(transaction.user_id, transaction.amount):
        return standard_response("Transacción no autorizada", False, 400)
    return standard_response({"detail": "Autorizada"}, True, 200)

@app.get("/users/me/")
async def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    user_data = schemas.UserResponse.model_validate(current_user).model_dump()
    return standard_response(user_data, True, 200)

@app.get("/me")
async def me(current_user: schemas.UserResponse = Depends(get_current_user)):
    user_data = schemas.UserResponse.model_validate(current_user).model_dump()
    return standard_response(user_data, True, 200)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error inesperado: {exc}")
    return standard_response("Error interno del servidor", False, 500)

# Personalizar el esquema OpenAPI para ocultar client_id/client_secret en Swagger

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    # Eliminar client_id y client_secret de /login
    if "/login/" in openapi_schema.get("paths", {}):
        post = openapi_schema["paths"]["/login/"]["post"]
        if "requestBody" in post:
            content = post["requestBody"]["content"]
            if "application/x-www-form-urlencoded" in content:
                schema = content["application/x-www-form-urlencoded"]["schema"]
                props = schema.get("properties", {})
                props.pop("client_id", None)
                props.pop("client_secret", None)
                # También eliminamos de required si están
                if "required" in schema:
                    schema["required"] = [r for r in schema["required"] if r not in ("client_id", "client_secret")]
    # Eliminar client_id/client_secret de parámetros de seguridad globales
    if "components" in openapi_schema and "securitySchemes" in openapi_schema["components"]:
        for scheme in openapi_schema["components"]["securitySchemes"].values():
            if "flows" in scheme and "password" in scheme["flows"]:
                pw = scheme["flows"]["password"]
                if "scopes" in pw:
                    pw["scopes"] = {}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
