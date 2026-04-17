# routers/expenses.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas
from ml.anomaly_detector import predict_for_user, train_for_user
from typing import List

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("", response_model=List[schemas.ExpenseOut])
def get_expenses(
    db:           Session      = Depends(get_db),
    current_user: models.User  = Depends(get_current_user)
):
    return db.query(models.Expense)\
             .filter(models.Expense.user_id == current_user.id)\
             .order_by(models.Expense.created_at.desc())\
             .all()


@router.post("", response_model=schemas.ExpenseOut)
def add_expense(
    expense_in:   schemas.ExpenseCreate,
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Save expense
    expense = models.Expense(**expense_in.dict(), user_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)

    # Run anomaly detection
    is_anomaly, score     = predict_for_user(current_user.id, expense_in.dict())
    expense.is_anomaly    = is_anomaly
    expense.anomaly_score = score
    db.commit()
    db.refresh(expense)

    # Retrain every 10 expenses
    count = db.query(models.Expense)\
              .filter(models.Expense.user_id == current_user.id)\
              .count()
    if count % 10 == 0:
        all_expenses = db.query(models.Expense)\
                         .filter(models.Expense.user_id == current_user.id)\
                         .all()
        train_for_user(current_user.id, [
            {"amount": e.amount, "category": e.category, "date": e.date}
            for e in all_expenses
        ])

    return expense


@router.get("/anomalies", response_model=List[schemas.ExpenseOut])
def get_anomalies(
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Expense)\
             .filter(
                 models.Expense.user_id   == current_user.id,
                 models.Expense.is_anomaly == True
             ).all()