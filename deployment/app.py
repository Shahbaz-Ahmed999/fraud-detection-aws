# app.py - Fraud Detection REST API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
from typing import List
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time credit card fraud detection using Machine Learning",
    version="1.0.0"
)

# Load model and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'saved_models', 'xgboost_tuned.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'saved_models', 'scaler.pkl')

print(f"Loading model from: {MODEL_PATH}")
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

print(f"Loading scaler from: {SCALER_PATH}")
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

print("✅ Model and scaler loaded successfully!")

# Define input schema
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

def prepare_features(transaction: dict) -> pd.DataFrame:
    """Prepare features exactly as done in preprocessing."""
    df = pd.DataFrame([transaction])

    # Feature engineering (same as preprocessing notebook)
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Is_Night'] = ((df['Hour'] >= 22) | (df['Hour'] <= 6)).astype(int)
    df['Is_Dawn'] = ((df['Hour'] >= 1) | (df['Hour'] <= 5)).astype(int)
    df['Amount_log'] = np.log1p(df['Amount'])
    df['Is_Zero_Amount'] = (df['Amount'] == 0).astype(int)
    df['Is_Large_Amount'] = (df['Amount'] > 1000).astype(int)
    df['Amount_Bin'] = pd.cut(df['Amount'],
                               bins=[0, 10, 50, 200, 1000, 99999],
                               labels=[0, 1, 2, 3, 4],
                               include_lowest=True).astype(int)

    # Scale Time, Amount, Amount_log
    df[['Time', 'Amount', 'Amount_log']] = scaler.transform(
        df[['Time', 'Amount', 'Amount_log']]
    )

    # Ensure correct column order
    feature_cols = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7',
                    'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15',
                    'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23',
                    'V24', 'V25', 'V26', 'V27', 'V28', 'Amount', 'Hour',
                    'Is_Night', 'Is_Dawn', 'Amount_log', 'Is_Zero_Amount',
                    'Is_Large_Amount', 'Amount_Bin']

    return df[feature_cols]

# API Endpoints
@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running!",
        "version": "1.0.0",
        "endpoints": ["/predict", "/health", "/docs"]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "XGBoost (Tuned)",
        "features": 37
    }

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        # Prepare features
        features = prepare_features(transaction.dict())

        # Get prediction and probability
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        fraud_probability = round(float(probability[1]), 4)
        is_fraud = bool(prediction == 1)

        # Risk level
        if fraud_probability >= 0.8:
            risk_level = "HIGH"
        elif fraud_probability >= 0.5:
            risk_level = "MEDIUM"
        elif fraud_probability >= 0.3:
            risk_level = "LOW"
        else:
            risk_level = "VERY LOW"

        return {
            "is_fraud": is_fraud,
            "fraud_probability": fraud_probability,
            "risk_level": risk_level,
            "recommendation": "BLOCK" if is_fraud else "APPROVE",
            "model_version": "2.0.0"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)