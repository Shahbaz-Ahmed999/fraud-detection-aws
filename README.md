# 💳 Credit Card Fraud Detection System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end machine learning system for real-time credit card fraud detection, trained on 283,726 transactions and served via a REST API.

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
Raw Data → EDA → Feature Engineering → SMOTE Balancing →
Model Training → Hyperparameter Tuning (Optuna) → Evaluation
```

### Inference Pipeline
```
Transaction (JSON) → FastAPI → Feature Engineering →
XGBoost Prediction → Risk Score → Response (JSON)
```

### Tech Stack
- **ML**: XGBoost, scikit-learn, LightGBM, imbalanced-learn, SHAP
- **Tuning**: Optuna (Bayesian optimization)
- **API**: FastAPI, Uvicorn
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
│   └── app.py                     # FastAPI REST API
├── models/saved_models/
│   ├── xgboost_tuned.pkl          # Primary model
│   ├── scaler.pkl                 # RobustScaler
│   └── model_config.json          # Model configuration
├── data/
│   ├── raw/                       # Original Kaggle dataset
│   └── processed/                 # Cleaned & split datasets
└── docs/                          # Plots & visualizations
```

---

## 🚀 Getting Started

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
Run notebooks in order: `01_eda` → `02_preprocessing` → `03_modeling` → `04_evaluation`

### 4. Start API
```bash
cd deployment
python app.py
```

---

## 💻 API

### Predict Endpoint
**POST** `/predict`

```json
{
  "Time": 406.0,
  "Amount": 149.62,
  "V1": -2.3122,
  "V2": 1.9519,
  "..."
}
```

### Response
```json
{
  "is_fraud": true,
  "fraud_probability": 0.9993,
  "risk_level": "HIGH",
  "recommendation": "BLOCK",
  "model_version": "2.0.0"
}
```

| Risk Level | Probability | Action |
|------------|-------------|--------|
| VERY LOW | < 30% | APPROVE |
| LOW | 30–50% | APPROVE |
| MEDIUM | 50–80% | REVIEW |
| HIGH | > 80% | BLOCK |

---

## 📈 Model Comparison

| Model | Precision | Recall | F1 | False Positives |
|-------|-----------|--------|----|-----------------|
| Logistic Regression | 0.063 | 0.915 | 0.118 | 964 |
| Random Forest | 0.566 | 0.845 | 0.678 | 46 |
| XGBoost | 0.518 | 0.831 | 0.638 | 55 |
| Random Forest (Tuned) | 0.714 | 0.845 | 0.774 | 24 |
| **XGBoost (Tuned) ✅** | **0.838** | **0.873** | **0.855** | **12** |

---

## 🔑 Key Technical Decisions

**Class Imbalance (599:1 ratio)** — Addressed using SMOTE oversampling applied exclusively to training data to prevent data leakage, balancing the dataset from 599:1 to 1:1.

**Evaluation Metric** — PR-AUC prioritized over accuracy, as the dataset is 99.83% legitimate transactions making accuracy a misleading metric.

**Hyperparameter Tuning** — Optuna Bayesian optimization over 30 trials, optimizing directly for PR-AUC on the validation set.

**Feature Scaling** — RobustScaler used over StandardScaler due to extreme outliers in the Amount feature (range: $0–$25,691).

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

*V1–V28 are PCA-transformed features (anonymized for privacy by original data providers.*

---

## 📊 Business Impact

Evaluated on held-out test set of 42,559 transactions:

- Fraud detected: **62 of 71 cases (87.3%)**
- False alarms: **12 legitimate transactions flagged**
- Legitimate transactions cleared: **42,483**

---

## 📚 Dataset

[Kaggle Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud) — European cardholders, September 2013, 284,807 transactions.

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
- [x] REST API (FastAPI)
- [ ] AWS Cloud Deployment
- [ ] Model Monitoring Dashboard
