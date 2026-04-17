# models.py
from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    expenses   = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount        = Column(Float, nullable=False)
    category      = Column(String, nullable=False)
    description   = Column(String, nullable=False)
    date          = Column(String, nullable=False)
    is_anomaly    = Column(Boolean, default=False)
    anomaly_score = Column(Float, default=0.0)
    created_at    = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="expenses")