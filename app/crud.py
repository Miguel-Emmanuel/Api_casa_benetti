from sqlalchemy.orm import Session
from . import schemas
from app.models.user import User
from app.models.transaction import Transaction
import bcrypt

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(email=user.email, password_hash=hashed_password.decode('utf-8'), name=getattr(user, 'name', ''))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        status=transaction.status,
        stripe_payment_id="test_stripe_id"  # Valor dummy para pruebas
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_user_transactions(db: Session, user_id: int, current_user=None):
    # Solo permite consultar transacciones propias si no es admin
    if current_user and current_user.role != "admin" and current_user.id != user_id:
        return []
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()
