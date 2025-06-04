from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    amount: int
    payment_method: str

class TransactionOut(BaseModel):
    id: int
    amount: int
    status: str
    stripe_payment_id: str
    created_at: datetime
    class Config:
        orm_mode = True
