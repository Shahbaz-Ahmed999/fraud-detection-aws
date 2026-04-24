# 💳 Credit Card Fraud Detection System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Deployed-orange.svg)](https://aws.amazon.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end machine learning system for real-time credit card fraud detection. Trained on 283,726 transactions, deployed serverlessly on AWS Lambda with a public REST API via API Gateway.

---

## ☁️ Live AWS Deployment

**Public API Endpoint:**
```
POST https://bz2tjixhwj.execute-api.us-east-1.amazonaws.com/prod/predict
```

**Example Request:**
```bash
curl -X POST https://bz2tjixhwj.execute-api.us-east-1.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"Time": 406.0, "Amount": 149.62, "V1": -2.3122, "V2": 1.9519, "V3": -1.6096,
       "V4": 3.9979, "V5": -0.5220, "V6": -1.4265, "V7": -2.5374, "V8": 1.3918,
       "V9": -2.7700, "V10": -2.7700, "V11": 3.2020, "V12": -2.8990, "V13": -0.5952,
       "V14": -4.2898, "V15": 0.3898, "V16": -1.1407, "V17": -2.8300, "V18": -0.0168,
       "V19": 0.4165, "V20": 0.1267, "V21": 0.5173, "V22": -0.0354, "V23": -0.4655,
       "V24": 0.3799, "V25": 0.1304, "V26": -0.1371, "V27": 0.3580, "V28": 0.0444}'
```

**Response:**
```json
{
  "is_fraud": true,
  "fraud_probability": 0.9993,
  "risk_level": "HIGH",
  "recommendation": "BLOCK",
  "model_version": "2.0.0"
}
```

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Precision** | 83.8% |
| **Recall** | 87.3% |
| **F1-Score** | 0.855 |
| **ROC-AUC** | 0.985 |
| **PR-AUC** | 0.873 |
| **False Alarms** | 12 per 42,559 transactions |

---

## 🏗️ System Architecture

### Training Pipeline
```
Raw Data (Kaggle) → EDA → Feature Engineering → SMOTE Balancing →
Model Training → Hyperparameter Tuning (Optuna) → Evaluation → S3
```

### Inference Pipeline
```
Request → API Gateway → AWS Lambda → S3 (load model) →
XGBoost Prediction → Risk Score → JSON Response
```

### AWS Infrastructure

| Service | Purpose |
|---------|---------|
| **S3** | Model artifacts & dataset storage |
| **Lambda** | Serverless ML inference (512MB, 60s timeout) |
| **API Gateway** | Public REST API endpoint |
| **CloudWatch** | Automatic logging & monitoring |
| **IAM** | Security & access management |

### Tech Stack
- **ML**: XGBoost, scikit-learn, LightGBM, imbalanced-learn, SHAP
- **Tuning**: Optuna (Bayesian optimization, 30 trials)
- **API**: FastAPI (local), AWS Lambda + API Gateway (cloud)
- **Cloud**: AWS (S3, Lambda, API Gateway, CloudWatch, IAM)
- **Analysis**: Pandas, NumPy, Matplotlib, Seaborn

---

## 📁 Project Structure

```
fraud-detection-aws/
├── notebooks/exploratory/
│   ├── 01_eda.ipynb               # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb     # Feature Engineering & SMOTE
│   ├── 03_modeling.ipynb          # Model Training & Tuning
│   └── 04_evaluation.ipynb        # SHAP Explainability
├── deployment/
│   ├── app.py                     # FastAPI REST API (local)
│   └── lambda_function.py         # AWS Lambda handler
├── models/saved_models/
│   ├── xgboost_tuned.pkl          # Primary model
│   ├── scaler.pkl                 # RobustScaler
│   └── model_config.json          # Model configuration
├── data/
│   ├── raw/                       # Original Kaggle dataset
│   └── processed/                 # Cleaned & split datasets
├── aws/                           # AWS setup scripts
└── docs/                          # Plots & visualizations
```

---

## 🚀 Local Setup

### 1. Clone & Setup
```bash
git clone https://github.com/Shahbaz-Ahmed999/fraud-detection-aws.git
cd fraud-detection-aws
python -m venv venv
venv\Scripts\activate
pip install numpy==1.26.4 pandas==2.2.2 scikit-learn xgboost lightgbm imbalanced-learn shap fastapi uvicorn optuna jupyter matplotlib seaborn
```

### 2. Download Dataset
Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud) and place in `data/raw/`.

### 3. Run Notebooks
```bash
jupyter notebook
```
Run in order: `01_eda` → `02_preprocessing` → `03_modeling` → `04_evaluation`

### 4. Start Local API
```bash
cd deployment
python app.py
```

---

## 💻 API Reference

### Predict Endpoint
**POST** `/predict`

**Request Body:** All 30 features required — `Time`, `Amount`, and `V1`–`V28`.

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `is_fraud` | boolean | Fraud classification |
| `fraud_probability` | float | Model confidence (0–1) |
| `risk_level` | string | VERY LOW / LOW / MEDIUM / HIGH |
| `recommendation` | string | APPROVE or BLOCK |
| `model_version` | string | Model version |

**Risk Level Thresholds:**

| Level | Probability | Action |
|-------|-------------|--------|
| VERY LOW | < 30% | APPROVE |
| LOW | 30–50% | APPROVE |
| MEDIUM | 50–80% | REVIEW |
| HIGH | > 80% | BLOCK |

---

## 📈 Model Development

| Model | Precision | Recall | F1 | False Positives |
|-------|-----------|--------|----|-----------------|
| Logistic Regression (baseline) | 0.063 | 0.915 | 0.118 | 964 |
| Random Forest | 0.566 | 0.845 | 0.678 | 46 |
| XGBoost | 0.518 | 0.831 | 0.638 | 55 |
| Random Forest (Tuned) | 0.714 | 0.845 | 0.774 | 24 |
| **XGBoost (Tuned) ✅** | **0.838** | **0.873** | **0.855** | **12** |

---

## 🔑 Key Technical Decisions

**Class Imbalance (599:1 ratio)** — SMOTE oversampling applied exclusively to training data to prevent data leakage, balancing from 599:1 to 1:1.

**Evaluation Metric** — PR-AUC prioritized over accuracy. With 99.83% legitimate transactions, accuracy is a misleading metric for fraud detection.

**Hyperparameter Tuning** — Optuna Bayesian optimization over 30 trials, optimizing directly for PR-AUC on the validation set.

**Feature Scaling** — RobustScaler over StandardScaler due to extreme outliers in Amount (range: $0–$25,691).

**Serverless Deployment** — AWS Lambda chosen for pay-per-request pricing, automatic scaling, and zero server management. Model artifacts stored in S3 and loaded on cold start.

---

## 🔍 SHAP Feature Importance

Top fraud indicators identified via SHAP analysis:

| Rank | Feature | Impact |
|------|---------|--------|
| 1 | V14 | Low values strongly indicate fraud |
| 2 | V12 | Low values strongly indicate fraud |
| 3 | V4 | High values indicate fraud |
| 4 | V10 | Low values indicate fraud |
| 5 | V17 | Low values indicate fraud |

*V1–V28 are PCA-transformed features, anonymized by the original data providers.*

---

## 📊 Business Impact

Evaluated on held-out test set of 42,559 transactions:

- Fraud detected: **62 of 71 cases (87.3%)**
- False alarms: **12 legitimate transactions flagged (0.028%)**
- Legitimate transactions cleared: **42,483**

---

## 📚 Dataset

[Kaggle Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud) — European cardholders, September 2013, 284,807 transactions, 0.17% fraud rate.

---

## 👤 Author

**Shahbaz Ahmed** — [GitHub](https://github.com/Shahbaz-Ahmed999)

---

## 📌 Roadmap

- [x] Exploratory Data Analysis
- [x] Feature Engineering & SMOTE
- [x] Model Training & Comparison (4 models)
- [x] Hyperparameter Tuning (Optuna)
- [x] SHAP Explainability
- [x] Local REST API (FastAPI)
- [x] AWS S3 — Model & data storage
- [x] AWS Lambda — Serverless deployment
- [x] AWS API Gateway — Public endpoint
- [x] AWS CloudWatch — Logging & monitoring
- [ ] Model Monitoring Dashboard
- [ ] Automated Retraining Pipeline
