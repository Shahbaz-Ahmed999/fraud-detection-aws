# 💳 Credit Card Fraud Detection System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-green.svg)](https://fastapi.tiangolo.com/)

Real-time machine learning system for detecting fraudulent credit card transactions, served via a REST API built with FastAPI.

---

## 🎯 Project Overview

This project implements an end-to-end fraud detection pipeline that:
- Detects **87% of fraudulent transactions** with **84% precision**
- Processes predictions in real-time via REST API
- Handles extreme class imbalance (0.17% fraud rate, 599:1 ratio)
- Provides explainable predictions using SHAP values
- Trained and evaluated on 283,726 real credit card transactions

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| **Precision** | 83.8% |
| **Recall** | 87.3% |
| **F1-Score** | 0.855 |
| **ROC-AUC** | 0.985 |
| **PR-AUC** | 0.873 |
| **False Alarms** | 12 per 42,559 transactions |

---

## 🏗️ Architecture

### Training Pipeline
```
Raw Data (Kaggle CSV) → EDA → Feature Engineering →
SMOTE Balancing → Model Training → Hyperparameter Tuning (Optuna) →
Evaluation → Saved Model (.pkl)
```

### Inference Pipeline
```
Transaction (JSON) → FastAPI → Feature Engineering →
XGBoost Prediction → Risk Level → Response (JSON)
```

### Tech Stack
- **ML**: scikit-learn, XGBoost, LightGBM, SHAP, imbalanced-learn
- **API**: FastAPI, Uvicorn
- **Tuning**: Optuna
- **Visualization**: Matplotlib, Seaborn

---

## 📁 Project Structure

```
fraud-detection-aws/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/                         # Visualizations & documentation
│   ├── class_distribution.png
│   ├── amount_analysis.png
│   ├── time_analysis.png
│   ├── correlation_analysis.png
│   ├── smote_comparison.png
│   ├── model_comparison.png
│   ├── shap_feature_importance.png
│   ├── shap_summary_dot.png
│   ├── confusion_matrix.png
│   └── threshold_tuning.png
│
├── data/
│   ├── raw/                      # Original Kaggle CSV
│   └── processed/                # Cleaned & split datasets
│
├── notebooks/
│   └── exploratory/
│       ├── 01_eda.ipynb
│       ├── 02_preprocessing.ipynb
│       ├── 03_modeling.ipynb
│       └── 04_evaluation.ipynb
│
├── models/
│   └── saved_models/
│       ├── final_model_xgb.pkl   # Primary model
│       ├── scaler.pkl            # RobustScaler
│       └── model_config.json     # Threshold config
│
└── deployment/
    └── app.py                    # FastAPI application
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Git

### 1. Clone Repository
```bash
git clone https://github.com/Shahbaz-Ahmed999/fraud-detection-aws.git
cd fraud-detection-aws
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install numpy==1.26.4 pandas==2.2.2 matplotlib seaborn scikit-learn xgboost lightgbm imbalanced-learn shap fastapi uvicorn pydantic optuna jupyter
```

### 4. Download Dataset
1. Go to [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud)
2. Download `creditcard.csv`
3. Place in `data/raw/` folder

### 5. Run Notebooks in Order
```bash
jupyter notebook
```
- `01_eda.ipynb` — Exploratory Data Analysis
- `02_preprocessing.ipynb` — Feature Engineering & SMOTE
- `03_modeling.ipynb` — Model Training & Tuning
- `04_evaluation.ipynb` — SHAP Explainability

### 6. Start API Server
```bash
cd deployment
python app.py
```
API runs at: `http://localhost:8000`
Docs at: `http://localhost:8000/docs`

---

## 💻 API Usage

### Predict Single Transaction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 406.0,
    "Amount": 149.62,
    "V1": -2.3122,
    "V2": 1.9519,
    ...
  }'
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

### Risk Levels
| Level | Probability | Action |
|-------|-------------|--------|
| VERY LOW | < 30% | APPROVE |
| LOW | 30-50% | APPROVE |
| MEDIUM | 50-80% | REVIEW |
| HIGH | > 80% | BLOCK |

---

## 📈 Model Development Journey

| Model | Precision | Recall | F1 | False Positives |
|-------|-----------|--------|----|-----------------|
| Logistic Regression (baseline) | 0.063 | 0.915 | 0.118 | 964 |
| Random Forest | 0.566 | 0.845 | 0.678 | 46 |
| XGBoost (default) | 0.518 | 0.831 | 0.638 | 55 |
| Random Forest (Tuned) | 0.714 | 0.845 | 0.774 | 24 |
| **XGBoost (Tuned) ✅** | **0.838** | **0.873** | **0.855** | **12** |

---

## 🔑 Key Technical Decisions

### Why XGBoost?
- Outperforms Random Forest on PR-AUC (0.873 vs 0.819)
- Better handling of imbalanced tabular data
- Faster inference for real-time API
- Tunable with Optuna for optimal performance

### Why Precision-Recall over Accuracy?
- Dataset is 99.83% legitimate transactions
- Accuracy is misleading — a model predicting all legitimate gets 99.83% accuracy
- PR-AUC focuses on minority class (fraud) performance
- F1-Score balances precision and recall fairly

### Why SMOTE?
- Original ratio: 599:1 (legitimate:fraud)
- SMOTE balanced training data to 1:1
- Applied ONLY to training data to prevent data leakage
- Improved F1 from ~0.12 (baseline) to 0.855

### Why RobustScaler?
- Dataset has extreme outliers (Amount up to $25,691)
- RobustScaler uses median/IQR instead of mean/std
- More resistant to outliers than StandardScaler

---

## 🔍 Model Explainability (SHAP)

Top fraud indicators identified by SHAP analysis:

| Rank | Feature | Direction |
|------|---------|-----------|
| 1 | V14 | Low values = fraud |
| 2 | V12 | Low values = fraud |
| 3 | V4 | High values = fraud |
| 4 | V10 | Low values = fraud |
| 5 | V17 | Low values = fraud |

Note: V1-V28 are PCA-transformed features (anonymized for privacy).

---

## 📊 Business Impact

Per 42,559 transactions:
- **Fraud caught**: 62 out of 71 cases (87.3%)
- **Fraud missed**: 9 cases
- **False alarms**: 12 (0.028% of legitimate transactions)
- **Legitimate cleared**: 42,483

---

## 🎓 Interview Talking Points

**"Tell me about this project"**
> "I built an end-to-end fraud detection system on the Kaggle credit card dataset — 284,807 transactions with only 0.17% fraud. The biggest challenge was class imbalance at 599:1, which I solved using SMOTE for oversampling and switching evaluation metrics from accuracy to Precision-Recall. I trained and compared 4 models — Logistic Regression, Random Forest, XGBoost, and LightGBM — then used Optuna for Bayesian hyperparameter tuning on XGBoost. The final model achieves 83.8% precision, 87.3% recall, and 0.855 F1-score, deployed as a real-time REST API using FastAPI."

**"How did you handle class imbalance?"**
> "Three approaches: First, SMOTE oversampling on training data only to avoid data leakage — this balanced the 599:1 ratio to 1:1. Second, cost-sensitive learning using class_weight='balanced' in baseline models. Third, switching from accuracy to PR-AUC as the primary evaluation metric, since accuracy is misleading when 99.83% of data is one class."

**"Why XGBoost over Random Forest?"**
> "Both performed well, but XGBoost with Optuna tuning achieved better PR-AUC (0.873 vs 0.819) which is the most important metric for imbalanced datasets. XGBoost also had fewer false positives — only 12 vs 24 for Random Forest — meaning fewer legitimate customers incorrectly flagged."

---

## 📚 Resources

- [Dataset: Kaggle Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Optuna Hyperparameter Tuning](https://optuna.org/)
- [Imbalanced-learn SMOTE](https://imbalanced-learn.org/)

---

## 👤 Author

**Shahbaz Ahmed**
- GitHub: [Shahbaz-Ahmed999](https://github.com/Shahbaz-Ahmed999)

---

## 📌 Project Status

**Status**: ✅ Complete

- [x] Exploratory Data Analysis
- [x] Feature Engineering & SMOTE
- [x] Model Training & Comparison
- [x] Hyperparameter Tuning (Optuna)
- [x] SHAP Explainability
- [x] REST API Deployment (FastAPI)
- [ ] AWS Cloud Deployment (planned)
- [ ] Model Monitoring Dashboard (planned)

**Last Updated**: April 2026

---

<div align="center">
  <strong>Built with 🧠 XGBoost | ⚡ FastAPI | 🐍 Python 3.11</strong>
</div>
