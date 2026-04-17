
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib, os

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

CATEGORIES = ['food','transport','shopping','health','entertainment','travel','other']

def model_path(user_id: int) -> str:
    return f"{MODEL_DIR}/user_{user_id}.pkl"

def prepare_features(expenses: list[dict]) -> np.ndarray:
    df = pd.DataFrame(expenses)
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    df['month']       = pd.to_datetime(df['date']).dt.month
    le = LabelEncoder()
    le.fit(CATEGORIES)
    df['category_enc'] = df['category'].apply(
        lambda x: le.transform([x])[0] if x in CATEGORIES else 0
    )
    return df[['amount', 'day_of_week', 'month', 'category_enc']].values

def train_for_user(user_id: int, expenses: list[dict]) -> bool:
    if len(expenses) < 20:
        return False
    X     = prepare_features(expenses)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    joblib.dump(model, model_path(user_id))
    return True

def predict_for_user(user_id: int, expense: dict) -> tuple[bool, float]:
    path = model_path(user_id)
    if not os.path.exists(path):
        return False, 0.0
    model     = joblib.load(path)
    X         = prepare_features([expense])
    score     = float(model.score_samples(X)[0])
    is_anomaly = model.predict(X)[0] == -1
    return is_anomaly, score
    
  