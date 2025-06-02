from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    status: str = "pending"
