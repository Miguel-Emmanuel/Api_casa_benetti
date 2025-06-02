from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)  # Especificar longitud para MySQL
    password = Column(String(255))  # Especificar longitud para MySQL

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    status = Column(String(50))  # Especificar longitud para MySQL
