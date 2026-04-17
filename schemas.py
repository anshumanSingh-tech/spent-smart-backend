# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str
    date: str

class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    date: str
    is_anomaly: bool
    anomaly_score: float
    created_at: datetime

    class Config:
        from_attributes = True