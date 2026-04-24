import streamlit as st
import requests
import json
import pandas as pd
import numpy as np

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ─────────────────────────────────────────
# API CONFIGURATION
# ─────────────────────────────────────────
API_URL = "https://bz2tjixhwj.execute-api.us-east-1.amazonaws.com/prod/predict"

# ─────────────────────────────────────────
# SAMPLE TRANSACTIONS (for demo)
# ─────────────────────────────────────────
FRAUD_SAMPLE = {
    "Time": 406.0, "Amount": 149.62,
    "V1": -2.3122, "V2": 1.9519, "V3": -1.6096, "V4": 3.9979,
    "V5": -0.5220, "V6": -1.4265, "V7": -2.5374, "V8": 1.3918,
    "V9": -2.7700, "V10": -2.7700, "V11": 3.2020, "V12": -2.8990,
    "V13": -0.5952, "V14": -4.2898, "V15": 0.3898, "V16": -1.1407,
    "V17": -2.8300, "V18": -0.0168, "V19": 0.4165, "V20": 0.1267,
    "V21": 0.5173, "V22": -0.0354, "V23": -0.4655, "V24": 0.3799,
    "V25": 0.1304, "V26": -0.1371, "V27": 0.3580, "V28": 0.0444
}

LEGIT_SAMPLE = {
    "Time": 10000.0, "Amount": 25.50,
    "V1": 1.2, "V2": 0.5, "V3": 0.8, "V4": 0.3,
    "V5": 0.1, "V6": -0.2, "V7": 0.4, "V8": 0.1,
    "V9": -0.1, "V10": 0.2, "V11": 0.3, "V12": 0.5,
    "V13": 0.1, "V14": 0.8, "V15": 0.2, "V16": 0.1,
    "V17": 0.3, "V18": 0.1, "V19": 0.2, "V20": 0.1,
    "V21": 0.0, "V22": 0.1, "V23": 0.0, "V24": 0.1,
    "V25": 0.2, "V26": 0.1, "V27": 0.0, "V28": 0.0
}

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("💳 Credit Card Fraud Detection System")
st.markdown("**Real-time ML fraud detection powered by XGBoost + AWS Lambda**")
st.markdown("---")

# ─────────────────────────────────────────
# SIDEBAR - PROJECT INFO
# ─────────────────────────────────────────
with st.sidebar:
    st.header("📊 Model Information")
    st.metric("Precision", "83.8%")
    st.metric("Recall", "87.3%")
    st.metric("F1-Score", "0.855")
    st.metric("PR-AUC", "0.873")

    st.markdown("---")
    st.header("☁️ AWS Infrastructure")
    st.markdown("- **Model**: XGBoost (Optuna tuned)")
    st.markdown("- **Deployment**: AWS Lambda")
    st.markdown("- **API**: AWS API Gateway")
    st.markdown("- **Storage**: AWS S3")
    st.markdown("- **Monitoring**: CloudWatch")

    st.markdown("---")
    st.header("📁 Quick Load")
    if st.button("🚨 Load Fraud Sample"):
        st.session_state.sample = "fraud"
    if st.button("✅ Load Legit Sample"):
        st.session_state.sample = "legit"
    if st.button("🔀 Load Random Sample"):
        st.session_state.sample = "random"

# ─────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔍 Single Prediction",
    "📊 Model Performance",
    "ℹ️ About"
])

# ══════════════════════════════════════════
# TAB 1: SINGLE PREDICTION
# ══════════════════════════════════════════
with tab1:
    st.subheader("Enter Transaction Details")

    # Load sample if button clicked
    sample_data = {}
    if st.session_state.get("sample") == "fraud":
        sample_data = FRAUD_SAMPLE
    elif st.session_state.get("sample") == "legit":
        sample_data = LEGIT_SAMPLE
    elif st.session_state.get("sample") == "random":
        sample_data = {
            "Time": np.random.uniform(0, 172792),
            "Amount": np.random.uniform(0, 500),
            **{f"V{i}": np.random.uniform(-3, 3) for i in range(1, 29)}
        }

    # ── Row 1: Basic Info ──
    col1, col2 = st.columns(2)
    with col1:
        time_val = st.number_input(
            "⏱️ Time (seconds since first transaction)",
            value=float(sample_data.get("Time", 406.0)),
            min_value=0.0, max_value=200000.0, step=1.0
        )
    with col2:
        amount_val = st.number_input(
            "💰 Transaction Amount ($)",
            value=float(sample_data.get("Amount", 149.62)),
            min_value=0.0, max_value=30000.0, step=0.01
        )

    # ── V Features in 4 columns ──
    st.markdown("**PCA Features (V1–V28)** *(anonymized for privacy)*")

    v_values = {}
    cols = st.columns(4)
    for i in range(1, 29):
        col_idx = (i - 1) % 4
        with cols[col_idx]:
            v_values[f"V{i}"] = st.number_input(
                f"V{i}",
                value=float(sample_data.get(f"V{i}", 0.0)),
                min_value=-20.0, max_value=20.0,
                step=0.0001, format="%.4f",
                key=f"v{i}"
            )

    st.markdown("---")

    # ── PREDICT BUTTON ──
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_clicked = st.button(
            "🔍 ANALYZE TRANSACTION",
            use_container_width=True,
            type="primary"
        )

    # ── PREDICTION RESULT ──
    if predict_clicked:
        # Build payload
        payload = {"Time": time_val, "Amount": amount_val}
        payload.update(v_values)

        with st.spinner("🔄 Calling AWS Lambda..."):
            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )
                result = response.json()

                st.markdown("---")
                st.subheader("🎯 Prediction Result")

                # ── Result Display ──
                is_fraud = result.get("is_fraud", False)
                probability = result.get("fraud_probability", 0)
                risk_level = result.get("risk_level", "UNKNOWN")
                recommendation = result.get("recommendation", "UNKNOWN")

                if is_fraud:
                    st.error("🚨 FRAUD DETECTED")
                else:
                    st.success("✅ LEGITIMATE TRANSACTION")

                # ── Metrics Row ──
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric(
                        "Fraud Probability",
                        f"{probability:.2%}"
                    )
                with m2:
                    st.metric("Risk Level", risk_level)
                with m3:
                    st.metric("Recommendation", recommendation)
                with m4:
                    st.metric(
                        "Model Version",
                        result.get("model_version", "2.0.0")
                    )

                # ── Probability Bar ──
                st.markdown("**Fraud Probability Score:**")
                st.progress(probability)

                # ── Risk Explanation ──
                st.markdown("---")
                st.subheader("📋 Risk Assessment")

                if probability >= 0.8:
                    st.error("""
                    **HIGH RISK** 🔴
                    - Fraud probability exceeds 80%
                    - Transaction should be BLOCKED immediately
                    - Alert customer and fraud team
                    - Matches known fraud patterns (V14, V12, V4)
                    """)
                elif probability >= 0.5:
                    st.warning("""
                    **MEDIUM RISK** 🟡
                    - Fraud probability between 50-80%
                    - Transaction flagged for manual review
                    - Contact customer to verify
                    """)
                elif probability >= 0.3:
                    st.info("""
                    **LOW RISK** 🟡
                    - Fraud probability between 30-50%
                    - Transaction approved with monitoring
                    - Log for pattern analysis
                    """)
                else:
                    st.success("""
                    **VERY LOW RISK** 🟢
                    - Fraud probability below 30%
                    - Transaction approved
                    - Normal transaction pattern
                    """)

                # ── Raw API Response ──
                with st.expander("🔧 Raw API Response (JSON)"):
                    st.json(result)

                # ── Transaction Summary ──
                with st.expander("📄 Transaction Summary"):
                    summary_df = pd.DataFrame([{
                        "Time": time_val,
                        "Amount": f"${amount_val:.2f}",
                        "Hour": f"{(time_val/3600) % 24:.1f}",
                        "Is_Night": "Yes" if ((time_val/3600) % 24 >= 22
                                    or (time_val/3600) % 24 <= 6) else "No",
                        "Fraud_Prob": f"{probability:.4f}",
                        "Decision": recommendation
                    }])
                    st.dataframe(summary_df, use_container_width=True)

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Lambda cold start can take 10-15 seconds. Please try again!")
            except requests.exceptions.ConnectionError:
                st.error("🌐 Connection error. Check your internet connection.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 The AWS API may need a moment to warm up. Please try again.")

# ══════════════════════════════════════════
# TAB 2: MODEL PERFORMANCE
# ══════════════════════════════════════════
with tab2:
    st.subheader("📊 Model Performance Dashboard")

    # ── Metrics Overview ──
    st.markdown("### Final Model: XGBoost (Optuna Tuned)")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Precision", "83.8%", "+27.2% vs RF")
    c2.metric("Recall", "87.3%", "+2.8% vs RF")
    c3.metric("F1-Score", "0.855", "+0.081 vs RF")
    c4.metric("PR-AUC", "0.873", "+0.054 vs RF")
    c5.metric("False Alarms", "12", "-34 vs RF")

    st.markdown("---")

    # ── Model Comparison Table ──
    st.markdown("### Model Comparison")
    comparison_data = {
        "Model": [
            "Logistic Regression (baseline)",
            "Random Forest",
            "XGBoost (default)",
            "Random Forest (Tuned)",
            "✅ XGBoost (Optuna Tuned)"
        ],
        "Precision": [0.063, 0.566, 0.518, 0.714, 0.838],
        "Recall": [0.915, 0.845, 0.831, 0.845, 0.873],
        "F1-Score": [0.118, 0.678, 0.638, 0.774, 0.855],
        "PR-AUC": [0.681, 0.819, 0.840, 0.750, 0.873],
        "False Positives": [964, 46, 55, 24, 12]
    }
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(
        df_comparison.style.highlight_max(
            subset=["Precision", "Recall", "F1-Score", "PR-AUC"],
            color="lightgreen"
        ).highlight_min(
            subset=["False Positives"],
            color="lightgreen"
        ),
        use_container_width=True
    )

    st.markdown("---")

    # ── Business Impact ──
    st.markdown("### 💰 Business Impact (Test Set: 42,559 transactions)")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Fraud Cases", "71 total")
    b2.metric("Detected", "62 (87.3%)")
    b3.metric("Missed", "9 (12.7%)")
    b4.metric("False Alarms", "12 (0.028%)")

    st.markdown("---")

    # ── SHAP Feature Importance ──
    st.markdown("### 🔍 Top Fraud Indicators (SHAP)")
    shap_data = pd.DataFrame({
        "Feature": ["V14", "V12", "V4", "V10", "V17",
                    "V3", "V11", "V16", "V2", "V7"],
        "SHAP Importance": [0.0830, 0.0637, 0.0607, 0.0505,
                            0.0398, 0.0376, 0.0349, 0.0282,
                            0.0114, 0.0102],
        "Direction": [
            "Low values = Fraud", "Low values = Fraud",
            "High values = Fraud", "Low values = Fraud",
            "Low values = Fraud", "Low values = Fraud",
            "High values = Fraud", "Low values = Fraud",
            "High values = Fraud", "Low values = Fraud"
        ]
    })
    st.dataframe(shap_data, use_container_width=True)

    st.markdown("---")

    # ── Data Pipeline ──
    st.markdown("### 🔄 ML Pipeline")
    st.markdown("""
    | Step | Details |
    |------|---------|
    | **Dataset** | 284,807 transactions, 0.17% fraud rate |
    | **Cleaning** | Removed 1,081 duplicates → 283,726 rows |
    | **Features** | 30 original + 7 engineered = 37 total |
    | **Imbalance** | SMOTE: 599:1 → 1:1 (training only) |
    | **Scaling** | RobustScaler on Time, Amount, Amount_log |
    | **Split** | 70% train / 15% val / 15% test (stratified) |
    | **Tuning** | Optuna: 30 trials, Bayesian optimization |
    | **Explainability** | SHAP TreeExplainer on 500 test samples |
    """)

# ══════════════════════════════════════════
# TAB 3: ABOUT
# ══════════════════════════════════════════
with tab3:
    st.subheader("ℹ️ About This Project")

    st.markdown("""
    ### 💳 Credit Card Fraud Detection System

    An end-to-end machine learning project demonstrating the complete
    data science workflow from raw data to production deployment.

    ### 🎯 Problem Statement
    Credit card fraud causes billions in annual losses. This system
    detects fraud in real-time with **87.3% recall** and **83.8% precision**,
    processing predictions in under 200ms via serverless AWS infrastructure.

    ### 🛠️ Technical Stack
    - **ML Model**: XGBoost tuned with Optuna (Bayesian optimization)
    - **Explainability**: SHAP values for model interpretability
    - **Imbalance Handling**: SMOTE oversampling (599:1 → 1:1)
    - **Cloud**: AWS Lambda + API Gateway + S3 + CloudWatch
    - **API**: REST API returning JSON predictions with risk levels

    ### 📊 Key Challenges Solved
    1. **Class Imbalance** — 99.83% legitimate, 0.17% fraud
    2. **Evaluation Metrics** — Used PR-AUC instead of accuracy
    3. **Feature Engineering** — 7 new features from Time and Amount
    4. **Serverless Deployment** — Docker for Linux package compatibility
    5. **Model Explainability** — SHAP for regulatory compliance

    ### 🔗 Links
    - [GitHub Repository](https://github.com/Shahbaz-Ahmed999/fraud-detection-aws)
    - [Live API Endpoint](https://bz2tjixhwj.execute-api.us-east-1.amazonaws.com/prod/predict)
    - [Dataset: Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)

    ### 👤 Author
    **Shahbaz Ahmed**
    - GitHub: [Shahbaz-Ahmed999](https://github.com/Shahbaz-Ahmed999)
    """)

    st.markdown("---")
    st.markdown("""
    ### 🎓 Interview Talking Points

    **"Tell me about this project"**
    > Built an end-to-end fraud detection system achieving 87.3% recall
    and 83.8% precision on 283,726 real transactions. Key challenges were
    handling 599:1 class imbalance using SMOTE, selecting PR-AUC over
    accuracy as evaluation metric, and deploying serverlessly on AWS Lambda
    with Docker for Linux compatibility. Model decisions are explainable
    via SHAP values.

    **"What was the hardest part?"**
    > The AWS deployment — specifically building Linux-compatible packages
    on Windows. Solved using Docker with the official AWS Lambda Python
    image to compile correct binaries, then published as a custom Lambda
    Layer. Reduced deployment package from 219MB to 2KB.

    **"Why XGBoost over other models?"**
    > XGBoost achieved the best PR-AUC (0.873) after Optuna tuning across
    30 trials. It handles tabular data efficiently, supports class weights,
    and provides SHAP-compatible feature importance — all critical for
    production fraud detection.
    """)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with 🧠 XGBoost | ☁️ AWS Lambda | 🐍 Python | "
    "📊 Streamlit | **Shahbaz Ahmed**"
)