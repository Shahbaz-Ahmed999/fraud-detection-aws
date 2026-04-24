import json
import boto3
import pickle
import numpy as np
import pandas as pd
import os
import tempfile

# S3 Configuration
BUCKET_NAME = "fraud-detection-ml-271369"
MODEL_KEY = "models/xgboost_tuned.pkl"
SCALER_KEY = "models/scaler.pkl"
CONFIG_KEY = "models/model_config.json"

# Global variables (loaded once, reused across invocations)
model = None
scaler = None
config = None

def load_artifacts():
    """Load model and scaler from S3."""
    global model, scaler, config
    
    if model is not None:
        return  # Already loaded - Lambda reuses this!
    
    print("Loading artifacts from S3...")
    s3 = boto3.client('s3')
    
    # Load model
    with tempfile.NamedTemporaryFile() as tmp:
        s3.download_fileobj(BUCKET_NAME, MODEL_KEY, tmp)
        tmp.seek(0)
        model = pickle.load(tmp)
    
    # Load scaler
    with tempfile.NamedTemporaryFile() as tmp:
        s3.download_fileobj(BUCKET_NAME, SCALER_KEY, tmp)
        tmp.seek(0)
        scaler = pickle.load(tmp)
    
    # Load config
    response = s3.get_object(Bucket=BUCKET_NAME, Key=CONFIG_KEY)
    config = json.loads(response['Body'].read().decode('utf-8'))
    
    print(f"Model loaded: {config.get('model_name', 'XGBoost')}")

def prepare_features(transaction: dict) -> pd.DataFrame:
    """Prepare features exactly as done in preprocessing."""
    df = pd.DataFrame([transaction])
    
    # Feature engineering (same as training)
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Is_Night'] = ((df['Hour'] >= 22) | (df['Hour'] <= 6)).astype(int)
    df['Is_Dawn'] = ((df['Hour'] >= 1) | (df['Hour'] <= 5)).astype(int)
    df['Amount_log'] = np.log1p(df['Amount'])
    df['Is_Zero_Amount'] = (df['Amount'] == 0).astype(int)
    df['Is_Large_Amount'] = (df['Amount'] > 1000).astype(int)
    df['Amount_Bin'] = pd.cut(
        df['Amount'],
        bins=[0, 10, 50, 200, 1000, 99999],
        labels=[0, 1, 2, 3, 4],
        include_lowest=True
    ).astype(int)
    
    # Scale features
    df[['Time', 'Amount', 'Amount_log']] = scaler.transform(
        df[['Time', 'Amount', 'Amount_log']]
    )
    
    # Correct column order (must match training exactly)
    feature_cols = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7',
                    'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15',
                    'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23',
                    'V24', 'V25', 'V26', 'V27', 'V28', 'Amount', 'Hour',
                    'Is_Night', 'Is_Dawn', 'Amount_log', 'Is_Zero_Amount',
                    'Is_Large_Amount', 'Amount_Bin']
    
    return df[feature_cols]

def lambda_handler(event, context):
    """Main Lambda handler - entry point for all requests."""
    
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    # Health check endpoint
    path = event.get('path', '/')
    if path == '/health':
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "healthy",
                "model": "XGBoost Fraud Detector v2.0",
                "endpoints": ["/predict", "/health"]
            })
        }
    
    # Main prediction endpoint
    try:
        # Load artifacts if not already loaded
        load_artifacts()
        
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        # Validate required fields
        required = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
        missing = [f for f in required if f not in body]
        if missing:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": f"Missing fields: {missing}"
                })
            }
        
        # Prepare features and predict
        features = prepare_features(body)
        probability = float(model.predict_proba(features)[0][1])
        prediction = int(probability >= 0.5)
        is_fraud = bool(prediction == 1)
        
        # Risk classification
        if probability >= 0.8:
            risk_level = "HIGH"
        elif probability >= 0.5:
            risk_level = "MEDIUM"
        elif probability >= 0.3:
            risk_level = "LOW"
        else:
            risk_level = "VERY LOW"
        
        # Build response
        response_body = {
            "is_fraud": is_fraud,
            "fraud_probability": round(probability, 4),
            "risk_level": risk_level,
            "recommendation": "BLOCK" if is_fraud else "APPROVE",
            "model_version": "2.0.0",
            "threshold_used": 0.5
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }