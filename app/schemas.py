from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Literal, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(default="user", max_length=32)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    role: str
    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0, description="El monto debe ser mayor a cero")
    status: Literal["pending", "completed", "failed"] = Field("pending", max_length=16)

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return v

    @field_validator("status")
    @classmethod
    def status_valid(cls, v):
        if v not in ("pending", "completed", "failed"):
            raise ValueError("Status inválido")
        return v

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
