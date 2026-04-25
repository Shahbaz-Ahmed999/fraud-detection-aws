import streamlit as st
import requests
import pandas as pd
import numpy as np

# ─────────────────────────────────────────
# PAGE CONFIGURATION (Must be first)
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Fraud Detection AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS - Professional Dark Theme
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global Font & Background ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide Streamlit Branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Main Container ── */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(99, 179, 237, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #a0aec0;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99, 179, 237, 0.15);
        border: 1px solid rgba(99, 179, 237, 0.4);
        color: #63b3ed;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 1rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #1a202c, #2d3748);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        transition: transform 0.2s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .metric-card:hover {
        transform: translateY(-2px);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #63b3ed;
        line-height: 1;
        margin-bottom: 0.3rem;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 500;
    }

    /* ── Section Headers ── */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2d3748;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Result Cards ── */
    .result-fraud {
        background: linear-gradient(135deg, #2d1515, #3d1a1a);
        border: 1px solid #fc8181;
        border-left: 4px solid #f56565;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
    }

    .result-legit {
        background: linear-gradient(135deg, #1a2d1a, #1a3d1a);
        border: 1px solid #68d391;
        border-left: 4px solid #48bb78;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
    }

    .result-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .result-subtitle {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    /* ── Info Cards ── */
    .info-card {
        background: #1a202c;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border: 1px solid #2d3748;
        margin-bottom: 0.8rem;
    }

    .info-card-title {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #718096;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    .info-card-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* ── AWS Badge ── */
    .aws-badge {
        background: linear-gradient(135deg, #f6821f, #d35400);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* ── Live indicator ── */
    .live-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }

    .live-text {
        color: #48bb78;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ── Probability Bar ── */
    .prob-bar-container {
        background: #2d3748;
        border-radius: 8px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    /* ── Sidebar Styling ── */
    .sidebar-metric {
        background: #1a202c;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #2d3748;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .sidebar-metric-label {
        font-size: 0.8rem;
        color: #718096;
    }

    .sidebar-metric-value {
        font-size: 0.95rem;
        font-weight: 700;
        color: #63b3ed;
    }

    /* ── Input Styling ── */
    .stNumberInput > div > div > input {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        color: #e2e8f0;
        border-radius: 8px;
    }

    /* ── Button Styling ── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.2rem;
    }

    /* ── Divider ── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #4a5568, transparent);
        margin: 1.5rem 0;
    }

    /* ── Feature Group Box ── */
    .feature-group {
        background: #1a202c;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #2d3748;
        margin-bottom: 1rem;
    }

    .feature-group-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: #63b3ed;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #4a5568;
        font-size: 0.8rem;
        border-top: 1px solid #2d3748;
        margin-top: 2rem;
    }

    /* ── Table Styling ── */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
API_URL = "https://bz2tjixhwj.execute-api.us-east-1.amazonaws.com/prod/predict"

FRAUD_SAMPLE = {
    "Time": 406.0, "Amount": 149.62,
    "V1": -2.3122, "V2": 1.9519,  "V3": -1.6096, "V4": 3.9979,
    "V5": -0.5220, "V6": -1.4265, "V7": -2.5374, "V8": 1.3918,
    "V9": -2.7700, "V10": -2.7700,"V11": 3.2020, "V12": -2.8990,
    "V13": -0.5952,"V14": -4.2898,"V15": 0.3898, "V16": -1.1407,
    "V17": -2.8300,"V18": -0.0168,"V19": 0.4165, "V20": 0.1267,
    "V21": 0.5173, "V22": -0.0354,"V23": -0.4655,"V24": 0.3799,
    "V25": 0.1304, "V26": -0.1371,"V27": 0.3580, "V28": 0.0444
}

LEGIT_SAMPLE = {
    "Time": 10000.0, "Amount": 25.50,
    "V1": 1.2,  "V2": 0.5,  "V3": 0.8,  "V4": 0.3,
    "V5": 0.1,  "V6": -0.2, "V7": 0.4,  "V8": 0.1,
    "V9": -0.1, "V10": 0.2, "V11": 0.3, "V12": 0.5,
    "V13": 0.1, "V14": 0.8, "V15": 0.2, "V16": 0.1,
    "V17": 0.3, "V18": 0.1, "V19": 0.2, "V20": 0.1,
    "V21": 0.0, "V22": 0.1, "V23": 0.0, "V24": 0.1,
    "V25": 0.2, "V26": 0.1, "V27": 0.0, "V28": 0.0
}

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def call_api(payload: dict) -> dict:
    """Call the AWS Lambda API."""
    response = requests.post(API_URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

def get_risk_color(risk_level: str) -> str:
    colors = {
        "HIGH": "#f56565",
        "MEDIUM": "#ed8936",
        "LOW": "#ecc94b",
        "VERY LOW": "#48bb78"
    }
    return colors.get(risk_level, "#718096")

def render_probability_bar(probability: float, risk_level: str):
    color = get_risk_color(risk_level)
    pct = probability * 100
    st.markdown(f"""
    <div style="margin: 0.8rem 0;">
        <div style="display:flex; justify-content:space-between;
                    margin-bottom:0.3rem;">
            <span style="font-size:0.8rem; color:#718096;">
                Fraud Probability
            </span>
            <span style="font-size:0.9rem; font-weight:700;
                         color:{color};">
                {pct:.1f}%
            </span>
        </div>
        <div style="background:#2d3748; border-radius:8px;
                    height:10px; overflow:hidden;">
            <div style="width:{pct}%; height:100%;
                        background:linear-gradient(90deg, {color}88, {color});
                        border-radius:8px; transition:width 0.5s ease;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem;">
        <div style="font-size:2.5rem;">🛡️</div>
        <div style="font-size:1.1rem; font-weight:700;
                    color:#e2e8f0;">FraudShield AI</div>
        <div style="font-size:0.75rem; color:#718096;
                    margin-top:0.2rem;">v2.0 — Production</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # Live Status
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <span class="live-dot"></span>
        <span class="live-text">API LIVE — AWS Lambda</span>
    </div>
    """, unsafe_allow_html=True)

    # Model Metrics
    st.markdown("**📊 Model Performance**")
    metrics = [
        ("Precision", "83.8%"),
        ("Recall", "87.3%"),
        ("F1-Score", "0.855"),
        ("PR-AUC", "0.873"),
        ("False Alarms", "12 / 42K"),
    ]
    for label, value in metrics:
        st.markdown(f"""
        <div class="sidebar-metric">
            <span class="sidebar-metric-label">{label}</span>
            <span class="sidebar-metric-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # AWS Stack
    st.markdown("**☁️ AWS Infrastructure**")
    aws_services = [
        ("⚡", "Lambda", "Serverless inference"),
        ("🌐", "API Gateway", "REST endpoint"),
        ("🗄️", "S3", "Model storage"),
        ("📊", "CloudWatch", "Monitoring"),
        ("🔐", "IAM", "Security"),
    ]
    for icon, service, desc in aws_services:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.6rem;
                    padding:0.4rem 0; border-bottom:1px solid #2d3748;">
            <span style="font-size:1rem;">{icon}</span>
            <div>
                <div style="font-size:0.8rem; font-weight:600;
                            color:#e2e8f0;">{service}</div>
                <div style="font-size:0.7rem; color:#718096;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # Quick Load Buttons
    st.markdown("**🎯 Quick Load Samples**")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚨 Fraud", use_container_width=True):
            st.session_state.sample = "fraud"
            st.rerun()
    with col_b:
        if st.button("✅ Legit", use_container_width=True):
            st.session_state.sample = "legit"
            st.rerun()
    if st.button("🔀 Random Transaction",
                 use_container_width=True):
        st.session_state.sample = "random"
        st.rerun()

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # Links
    st.markdown("**🔗 Project Links**")
    st.markdown("""
    - [📁 GitHub Repository](https://github.com/Shahbaz-Ahmed999/fraud-detection-aws)
    - [📊 Kaggle Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud)
    """)

# ─────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🛡️ Credit Card Fraud Detection</div>
    <div class="hero-subtitle">
        Production-grade ML system · Real-time inference ·
        Deployed on AWS Lambda
    </div>
    <div style="margin-top:1rem;">
        <span class="hero-badge">XGBoost</span>
        <span class="hero-badge">AWS Lambda</span>
        <span class="hero-badge">Optuna Tuned</span>
        <span class="hero-badge">SHAP Explainable</span>
        <span class="hero-badge">283K Transactions</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TOP METRICS ROW
# ─────────────────────────────────────────
cols = st.columns(5)
top_metrics = [
    ("83.8%", "Precision"),
    ("87.3%", "Recall"),
    ("0.855", "F1-Score"),
    ("0.873", "PR-AUC"),
    ("~200ms", "Latency"),
]
for col, (val, label) in zip(cols, top_metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔍  Predict Transaction",
    "📊  Model Analytics",
    "ℹ️  About & Interview Prep"
])

# ══════════════════════════════════════════
# TAB 1: PREDICTION
# ══════════════════════════════════════════
with tab1:

    # Load sample data
    sample_data = {}
    if st.session_state.get("sample") == "fraud":
        sample_data = FRAUD_SAMPLE
        st.info("🚨 Fraud sample loaded — this transaction will be flagged")
    elif st.session_state.get("sample") == "legit":
        sample_data = LEGIT_SAMPLE
        st.success("✅ Legitimate sample loaded — this transaction will be approved")
    elif st.session_state.get("sample") == "random":
        np.random.seed()
        sample_data = {
            "Time": np.random.uniform(0, 172792),
            "Amount": np.random.uniform(0, 500),
            **{f"V{i}": np.random.uniform(-3, 3) for i in range(1, 29)}
        }
        st.info("🔀 Random transaction loaded")

    # ── Section: Transaction Details ──
    st.markdown("""
    <div class="section-header">
        💳 Transaction Details
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        time_val = st.number_input(
            "⏱️ Time (seconds elapsed)",
            value=float(sample_data.get("Time", 406.0)),
            min_value=0.0, max_value=200000.0, step=1.0,
            help="Seconds since the first transaction in the dataset"
        )
        hour = (time_val / 3600) % 24
        st.caption(f"🕐 Equivalent hour: **{hour:.1f}:00** "
                   f"({'🌙 Night' if hour < 6 or hour >= 22 else '☀️ Day'})")

    with col2:
        amount_val = st.number_input(
            "💰 Transaction Amount (USD)",
            value=float(sample_data.get("Amount", 149.62)),
            min_value=0.0, max_value=30000.0, step=0.01,
            format="%.2f",
            help="Transaction amount in US dollars"
        )
        if amount_val > 1000:
            st.caption("⚠️ Large amount transaction detected")
        elif amount_val == 0:
            st.caption("⚠️ Zero-value transaction")
        else:
            st.caption(f"💵 Amount: **${amount_val:,.2f}**")

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">Amount Category</div>
            <div class="info-card-value">
                {'🔴 Large' if amount_val > 1000
                 else '🟡 Medium' if amount_val > 200
                 else '🟢 Small'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # ── Section: PCA Features ──
    st.markdown("""
    <div class="section-header">
        🔢 PCA Features (V1–V28)
        <span style="font-size:0.75rem; color:#718096; font-weight:400;
                     margin-left:0.5rem;">
            Anonymized for privacy · Auto-filled from samples
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ What are V1–V28 features?", expanded=False):
        st.markdown("""
        These are **28 anonymized features** created using
        **Principal Component Analysis (PCA)** by the original
        data providers (ULB Machine Learning Group) to protect
        cardholder privacy. The original features (card number,
        merchant, location) cannot be shared publicly.

        In production systems, these would be automatically
        computed from raw transaction data by the feature
        engineering pipeline.
        """)

    # V features in organized groups of 7
    v_values = {}
    group_labels = ["V1–V7", "V8–V14", "V15–V21", "V22–V28"]

    for group_idx, group_label in enumerate(group_labels):
        st.markdown(f"""
        <div class="feature-group-title"
             style="font-size:0.72rem; font-weight:600;
                    color:#63b3ed; text-transform:uppercase;
                    letter-spacing:1px; margin-top:0.8rem;
                    margin-bottom:0.4rem;">
            {group_label}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(7)
        start = group_idx * 7 + 1
        end = min(start + 7, 29)

        for i, col in zip(range(start, end), cols):
            with col:
                v_values[f"V{i}"] = st.number_input(
                    f"V{i}",
                    value=float(sample_data.get(f"V{i}", 0.0)),
                    min_value=-20.0, max_value=20.0,
                    step=0.0001, format="%.3f",
                    key=f"v{i}",
                    label_visibility="visible"
                )

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # ── PREDICT BUTTON ──
    col_l, col_m, col_r = st.columns([1.5, 2, 1.5])
    with col_m:
        predict_clicked = st.button(
            "⚡ ANALYZE TRANSACTION",
            use_container_width=True,
            type="primary"
        )
        st.caption(
            "🔒 Powered by AWS Lambda · Response in ~200ms"
        )

    # ── PREDICTION RESULT ──
    if predict_clicked:
        payload = {"Time": time_val, "Amount": amount_val}
        payload.update(v_values)

        with st.spinner("🔄 Sending to AWS Lambda for analysis..."):
            try:
                result = call_api(payload)

                is_fraud     = result.get("is_fraud", False)
                probability  = result.get("fraud_probability", 0)
                risk_level   = result.get("risk_level", "UNKNOWN")
                recommendation = result.get("recommendation", "UNKNOWN")

                st.markdown('<div class="custom-divider"></div>',
                            unsafe_allow_html=True)

                # ── Main Result Banner ──
                if is_fraud:
                    st.markdown(f"""
                    <div class="result-fraud">
                        <div class="result-title" style="color:#fc8181;">
                            🚨 FRAUD DETECTED
                        </div>
                        <div class="result-subtitle" style="color:#feb2b2;">
                            This transaction matches known fraud patterns.
                            Immediate action required.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-legit">
                        <div class="result-title" style="color:#68d391;">
                            ✅ LEGITIMATE TRANSACTION
                        </div>
                        <div class="result-subtitle" style="color:#9ae6b4;">
                            Transaction appears normal.
                            Approved for processing.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── 4 Result Metrics ──
                r1, r2, r3, r4 = st.columns(4)

                risk_color = get_risk_color(risk_level)
                rec_color = "#f56565" if is_fraud else "#48bb78"

                with r1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value"
                             style="color:{risk_color};">
                            {probability:.1%}
                        </div>
                        <div class="metric-label">
                            Fraud Probability
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with r2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value"
                             style="color:{risk_color};">
                            {risk_level}
                        </div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    """, unsafe_allow_html=True)
                with r3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value"
                             style="color:{rec_color};">
                            {recommendation}
                        </div>
                        <div class="metric-label">
                            Recommendation
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with r4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value"
                             style="color:#63b3ed;">
                            {result.get('model_version','2.0')}
                        </div>
                        <div class="metric-label">
                            Model Version
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Probability Bar ──
                render_probability_bar(probability, risk_level)

                # ── Risk Breakdown ──
                st.markdown('<div class="custom-divider"></div>',
                            unsafe_allow_html=True)
                st.markdown("""
                <div class="section-header">
                    📋 Risk Assessment Breakdown
                </div>
                """, unsafe_allow_html=True)

                ra1, ra2 = st.columns(2)
                with ra1:
                    # Risk scale visual
                    levels = [
                        ("VERY LOW",  "#48bb78", "< 30%",  "✅ Approve"),
                        ("LOW",       "#ecc94b", "30–50%", "✅ Approve"),
                        ("MEDIUM",    "#ed8936", "50–80%", "👁️ Review"),
                        ("HIGH",      "#f56565", "> 80%",  "🚫 Block"),
                    ]
                    st.markdown("**Risk Scale**")
                    for level, color, prob_range, action in levels:
                        is_current = (level == risk_level)
                        bg = f"rgba({color}, 0.15)" if is_current else "transparent"
                        border = f"2px solid {color}" if is_current else "1px solid #2d3748"
                        st.markdown(f"""
                        <div style="display:flex; justify-content:space-between;
                                    align-items:center; padding:0.5rem 0.8rem;
                                    border-radius:8px; margin-bottom:0.3rem;
                                    border:{border}; background:{bg};">
                            <span style="color:{color}; font-weight:600;
                                         font-size:0.85rem;">
                                {'▶ ' if is_current else ''}{level}
                            </span>
                            <span style="color:#718096; font-size:0.8rem;">
                                {prob_range}
                            </span>
                            <span style="font-size:0.8rem;">{action}</span>
                        </div>
                        """, unsafe_allow_html=True)

                with ra2:
                    st.markdown("**Transaction Analysis**")
                    hour_cat = ("🌙 Late Night (High Risk Period)"
                                if 1 <= hour <= 5
                                else "🌆 Evening"
                                if hour >= 18
                                else "☀️ Daytime (Low Risk Period)")
                    amt_cat  = ("🔴 Very Large (>$1000)"
                                if amount_val > 1000
                                else "🟡 Medium ($200–$1000)"
                                if amount_val > 200
                                else "🟢 Normal (<$200)")

                    analysis_items = [
                        ("Amount",   amt_cat),
                        ("Time",     hour_cat),
                        ("V14 Signal",
                         ("🔴 Anomalous"
                          if v_values.get("V14", 0) < -2
                          else "🟢 Normal")),
                        ("V12 Signal",
                         ("🔴 Anomalous"
                          if v_values.get("V12", 0) < -2
                          else "🟢 Normal")),
                        ("Decision",
                         f"{'🚫 BLOCK' if is_fraud else '✅ APPROVE'}"),
                    ]
                    for key, val in analysis_items:
                        st.markdown(f"""
                        <div style="display:flex;
                                    justify-content:space-between;
                                    padding:0.4rem 0;
                                    border-bottom:1px solid #2d3748;
                                    font-size:0.85rem;">
                            <span style="color:#718096;">{key}</span>
                            <span style="color:#e2e8f0;
                                         font-weight:500;">{val}</span>
                        </div>
                        """, unsafe_allow_html=True)

                # ── Expandable Details ──
                with st.expander("🔧 Raw API Response"):
                    st.json(result)

                with st.expander("📄 Transaction Summary"):
                    st.dataframe(pd.DataFrame([{
                        "Time (s)": time_val,
                        "Hour": f"{hour:.1f}",
                        "Amount": f"${amount_val:,.2f}",
                        "Is Night": "Yes" if hour < 6 or hour >= 22 else "No",
                        "Fraud Prob": f"{probability:.4f}",
                        "Risk": risk_level,
                        "Decision": recommendation,
                    }]), use_container_width=True, hide_index=True)

            except requests.exceptions.Timeout:
                st.error("""
                ⏱️ **Request timed out**

                Lambda cold starts can take 10–15 seconds on first call.
                Please wait a moment and try again.
                """)
            except requests.exceptions.ConnectionError:
                st.error("""
                🌐 **Connection Error**

                Cannot reach the AWS API. Please check your internet
                connection and try again.
                """)
            except Exception as e:
                st.error(f"❌ **Unexpected Error:** {str(e)}")
                st.info("💡 Try reloading the page or using a sample transaction.")

# ══════════════════════════════════════════
# TAB 2: MODEL ANALYTICS
# ══════════════════════════════════════════
with tab2:

    # ── Section: Model Journey ──
    st.markdown("""
    <div class="section-header">🏆 Model Development Journey</div>
    """, unsafe_allow_html=True)

    comparison_data = {
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "XGBoost (default)",
            "Random Forest (Tuned)",
            "✅ XGBoost + Optuna"
        ],
        "Precision": [0.063, 0.566, 0.518, 0.714, 0.838],
        "Recall":    [0.915, 0.845, 0.831, 0.845, 0.873],
        "F1-Score":  [0.118, 0.678, 0.638, 0.774, 0.855],
        "PR-AUC":    [0.681, 0.819, 0.840, 0.750, 0.873],
        "False Pos": [964,   46,    55,    24,    12],
        "Stage":     ["Baseline","Improved","Improved","Better","🏆 Final"]
    }
    df = pd.DataFrame(comparison_data)
    st.dataframe(
        df.style
          .highlight_max(subset=["Precision","Recall","F1-Score","PR-AUC"],
                         color="#1a3d1a")
          .highlight_min(subset=["False Pos"], color="#1a3d1a")
          .format({"Precision": "{:.3f}", "Recall": "{:.3f}",
                   "F1-Score": "{:.3f}",  "PR-AUC": "{:.3f}"}),
        use_container_width=True, hide_index=True
    )

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # ── Two Column Layout ──
    left, right = st.columns(2)

    with left:
        # Business Impact
        st.markdown("""
        <div class="section-header">
            💰 Business Impact (Test Set)
        </div>
        """, unsafe_allow_html=True)

        impact_items = [
            ("Total Transactions",  "42,559",    "#63b3ed"),
            ("Fraud Cases",         "71 total",  "#fc8181"),
            ("Fraud Detected ✅",   "62 (87.3%)","#68d391"),
            ("Fraud Missed ❌",     "9 (12.7%)", "#fc8181"),
            ("False Alarms",        "12 (0.028%)","#ecc94b"),
            ("Legit Cleared",       "42,483",    "#68d391"),
        ]
        for label, value, color in impact_items:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between;
                        align-items:center; padding:0.6rem 0.8rem;
                        border-radius:8px; margin-bottom:0.4rem;
                        background:#1a202c; border:1px solid #2d3748;">
                <span style="color:#a0aec0; font-size:0.85rem;">
                    {label}
                </span>
                <span style="color:{color}; font-weight:700;
                             font-size:0.9rem;">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    with right:
        # SHAP
        st.markdown("""
        <div class="section-header">
            🔍 SHAP Feature Importance
        </div>
        """, unsafe_allow_html=True)

        shap_features = [
            ("V14", 0.0830, "Low = Fraud"),
            ("V12", 0.0637, "Low = Fraud"),
            ("V4",  0.0607, "High = Fraud"),
            ("V10", 0.0505, "Low = Fraud"),
            ("V17", 0.0398, "Low = Fraud"),
            ("V3",  0.0376, "Low = Fraud"),
            ("V11", 0.0349, "High = Fraud"),
            ("V16", 0.0282, "Low = Fraud"),
        ]
        max_shap = shap_features[0][1]
        for feat, importance, direction in shap_features:
            bar_width = (importance / max_shap) * 100
            st.markdown(f"""
            <div style="margin-bottom:0.5rem;">
                <div style="display:flex; justify-content:space-between;
                            margin-bottom:0.2rem;">
                    <span style="font-size:0.8rem; font-weight:600;
                                 color:#e2e8f0;">{feat}</span>
                    <span style="font-size:0.75rem; color:#718096;">
                        {direction}
                    </span>
                    <span style="font-size:0.75rem; color:#63b3ed;">
                        {importance:.4f}
                    </span>
                </div>
                <div style="background:#2d3748; border-radius:4px;
                            height:6px; overflow:hidden;">
                    <div style="width:{bar_width}%; height:100%;
                                background:linear-gradient(
                                    90deg, #4299e1, #63b3ed);
                                border-radius:4px;">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>',
                unsafe_allow_html=True)

    # ── ML Pipeline ──
    st.markdown("""
    <div class="section-header">🔄 Complete ML Pipeline</div>
    """, unsafe_allow_html=True)

    pipeline_steps = [
        ("01", "Data Collection",    "Kaggle · 284,807 transactions · 0.17% fraud"),
        ("02", "EDA",                "Class imbalance · Time patterns · Correlations"),
        ("03", "Feature Engineering","7 new features: Hour, Is_Night, Amount_log, etc."),
        ("04", "Preprocessing",      "RobustScaler · 70/15/15 stratified split"),
        ("05", "SMOTE",              "Balanced 599:1 → 1:1 ratio (train only)"),
        ("06", "Model Training",     "4 algorithms: LR, RF, XGBoost, LightGBM"),
        ("07", "Optuna Tuning",      "Bayesian optimization · 30 trials · PR-AUC target"),
        ("08", "SHAP Analysis",      "TreeExplainer · Top feature identification"),
        ("09", "AWS Deployment",     "Lambda + API Gateway + S3 + CloudWatch"),
        ("10", "Monitoring",         "CloudWatch logs · Cold start tracking"),
    ]
    p1, p2 = st.columns(2)
    for i, (num, title, desc) in enumerate(pipeline_steps):
        col = p1 if i % 2 == 0 else p2
        with col:
            st.markdown(f"""
            <div style="display:flex; gap:0.8rem; align-items:flex-start;
                        padding:0.6rem; border-radius:8px; margin-bottom:0.4rem;
                        background:#1a202c; border:1px solid #2d3748;">
                <div style="background:#2b4c7e; color:#63b3ed;
                            border-radius:6px; padding:0.2rem 0.5rem;
                            font-size:0.7rem; font-weight:700;
                            min-width:28px; text-align:center;">
                    {num}
                </div>
                <div>
                    <div style="font-size:0.85rem; font-weight:600;
                                color:#e2e8f0;">{title}</div>
                    <div style="font-size:0.75rem; color:#718096;">
                        {desc}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 3: ABOUT
# ══════════════════════════════════════════
with tab3:
    a1, a2 = st.columns([3, 2])

    with a1:
        st.markdown("""
        <div class="section-header">🎯 Project Overview</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        An **end-to-end production ML system** built from scratch —
        covering the complete data science lifecycle from raw data
        exploration to cloud deployment with real-time API access.

        **Key challenges solved:**
        - 🔴 **599:1 class imbalance** — solved with SMOTE
        - 📊 **Misleading accuracy metric** — switched to PR-AUC
        - ⚙️ **Hyperparameter search** — Bayesian optimization (Optuna)
        - ☁️ **Linux packages on Windows** — solved with Docker
        - 🚀 **Serverless deployment** — AWS Lambda + API Gateway
        """)

        st.markdown('<div class="custom-divider"></div>',
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">🎓 Interview Q&A</div>
        """, unsafe_allow_html=True)

        qa_pairs = [
            (
                "Tell me about this project",
                "Built an end-to-end fraud detection system on 283,726 real "
                "transactions achieving 87.3% recall and 83.8% precision. "
                "Key challenges: 599:1 class imbalance (SMOTE), metric "
                "selection (PR-AUC over accuracy), Optuna hyperparameter "
                "tuning (30 trials), and serverless deployment on AWS Lambda "
                "using Docker for Linux package compatibility."
            ),
            (
                "Why PR-AUC over ROC-AUC?",
                "With 99.83% legitimate transactions, ROC-AUC is misleading "
                "because the huge true negative count makes FPR look "
                "artificially low. PR-AUC focuses on the minority class "
                "(fraud), giving an honest performance picture."
            ),
            (
                "How did you handle class imbalance?",
                "Three-pronged approach: (1) SMOTE oversampling applied ONLY "
                "to training data to prevent leakage, (2) class weights in "
                "models to penalize fraud misclassification, (3) threshold "
                "tuning optimized for business cost not default 0.5."
            ),
            (
                "Why XGBoost as final model?",
                "XGBoost achieved best PR-AUC (0.873) after Optuna tuning "
                "across 30 trials. It handles tabular data efficiently, "
                "supports native SHAP explainability, and with Bayesian "
                "optimization outperformed Random Forest by 10% on F1."
            ),
            (
                "How did you deploy to AWS?",
                "Lambda + API Gateway for serverless inference. Challenge: "
                "219MB deployment package exceeded limits. Solution: separated "
                "function code (2KB) from dependencies (Lambda Layer via "
                "Docker). Model loaded from S3 on cold start, cached in "
                "memory for subsequent calls."
            ),
            (
                "What would you improve?",
                "1) Velocity features (transactions/hour per card) — can't "
                "add with this dataset. 2) Automated monthly retraining with "
                "drift detection. 3) A/B testing framework for model updates. "
                "4) Real-time feature store for low-latency inference."
            ),
        ]

        for question, answer in qa_pairs:
            with st.expander(f"❓ {question}"):
                st.markdown(f"""
                <div style="background:#1a2d1a; border-left:3px solid #48bb78;
                            border-radius:0 8px 8px 0; padding:0.8rem 1rem;
                            color:#9ae6b4; font-size:0.9rem; line-height:1.6;">
                    {answer}
                </div>
                """, unsafe_allow_html=True)

    with a2:
        # Tech Stack
        st.markdown("""
        <div class="section-header">🛠️ Tech Stack</div>
        """, unsafe_allow_html=True)

        tech_categories = [
            ("Machine Learning", [
                "XGBoost 2.1.1",
                "scikit-learn 1.4.2",
                "LightGBM 4.6.0",
                "imbalanced-learn 0.14",
            ]),
            ("Optimization & XAI", [
                "Optuna (Bayesian)",
                "SHAP TreeExplainer",
                "30-trial search",
                "PR-AUC objective",
            ]),
            ("AWS Cloud", [
                "Lambda (serverless)",
                "API Gateway (REST)",
                "S3 (model storage)",
                "CloudWatch (logs)",
            ]),
            ("Data & Deployment", [
                "Pandas / NumPy",
                "Docker (Linux pkgs)",
                "Streamlit Cloud",
                "GitHub Actions",
            ]),
        ]

        for category, items in tech_categories:
            st.markdown(f"""
            <div class="info-card" style="margin-bottom:0.8rem;">
                <div class="info-card-title">{category}</div>
                {"".join([
                    f'<div style="font-size:0.82rem; color:#e2e8f0;'
                    f' padding:0.15rem 0;">• {item}</div>'
                    for item in items
                ])}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>',
                    unsafe_allow_html=True)

        # CV Bullets
        st.markdown("""
        <div class="section-header">📄 CV Bullet Points</div>
        """, unsafe_allow_html=True)

        cv_bullets = [
            "Built end-to-end fraud detection system on 283K transactions; "
            "deployed serverlessly on AWS Lambda achieving 87.3% recall, "
            "83.8% precision",
            "Resolved 599:1 class imbalance via SMOTE; optimized XGBoost "
            "with Optuna (30 Bayesian trials); improved F1 from 0.638→0.855",
            "Engineered REST API via AWS Lambda + API Gateway; reduced "
            "deployment package from 219MB→2KB using Docker layer strategy",
            "Applied SHAP explainability identifying V14, V12, V4 as top "
            "fraud signals; delivered risk-scored predictions with <200ms "
            "latency",
        ]
        for i, bullet in enumerate(cv_bullets, 1):
            st.markdown(f"""
            <div style="background:#1a202c; border-radius:8px;
                        padding:0.7rem 0.9rem; margin-bottom:0.5rem;
                        border-left:3px solid #63b3ed;
                        font-size:0.82rem; color:#e2e8f0; line-height:1.5;">
                <span style="color:#63b3ed; font-weight:700;">
                    {i}.
                </span> {bullet}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom:0.5rem;">
        🛡️ <strong>FraudShield AI</strong> · Credit Card Fraud Detection
    </div>
    <div>
        Built with 🧠 XGBoost · ☁️ AWS Lambda · 🐍 Python · 📊 Streamlit
        &nbsp;|&nbsp;
        <a href="https://github.com/Shahbaz-Ahmed999/fraud-detection-aws"
           style="color:#63b3ed; text-decoration:none;">
            GitHub ↗
        </a>
        &nbsp;|&nbsp;
        <strong>Shahbaz Ahmed</strong>
    </div>
</div>
""", unsafe_allow_html=True)
