# Credit Card Fraud Detection System
## Problem Statement Document

---

## 1. EXECUTIVE SUMMARY

### Business Problem
Credit card fraud causes billions of dollars in losses annually. Financial institutions need automated systems to detect fraudulent transactions in real-time while minimizing false alarms that frustrate legitimate customers.

### Proposed Solution
Develop a machine learning-based fraud detection system that:
- Classifies transactions as fraudulent or legitimate in real-time (<100ms)
- Achieves >90% fraud detection rate (Recall)
- Maintains <2% false positive rate (Precision >98%)
- Deploys on AWS cloud infrastructure for scalability

### Expected Impact
- Reduce fraud losses by 70-85%
- Improve customer trust and satisfaction
- Enable real-time transaction monitoring
- Provide explainable predictions for compliance

---

## 2. PROBLEM DEFINITION

### 2.1 Problem Type
**Binary Classification Problem**
- **Class 0 (Negative)**: Legitimate Transaction
- **Class 1 (Positive)**: Fraudulent Transaction

### 2.2 Input Features
Transaction-level features including:
- **Transaction Amount**: Dollar value
- **Time**: Timestamp of transaction
- **Anonymized Features**: V1-V28 (PCA-transformed for privacy)
- **Derived Features**: 
  - Time since last transaction
  - Transaction frequency
  - Deviation from average spending

### 2.3 Output
Binary prediction:
- `0` = Legitimate (allow transaction)
- `1` = Fraudulent (block/flag transaction)

### 2.4 Constraints
- **Latency**: Predictions must complete in <100ms
- **Availability**: 99.9% uptime required
- **Explainability**: Must justify flagged transactions
- **Data Privacy**: Cannot store raw customer PII
- **Cost**: Must operate within AWS Free Tier during development

---

## 3. BUSINESS CONTEXT

### 3.1 Stakeholders
- **Customers**: Want protection without inconvenience
- **Fraud Team**: Needs accurate flags for investigation
- **Business Team**: Balances security with customer experience
- **Compliance**: Requires audit trail and explainability
- **Engineering**: Needs maintainable, scalable system

### 3.2 Current Situation
- **Manual Review**: Slow, expensive, doesn't scale
- **Rule-Based Systems**: Rigid, high false positive rate (5-10%)
- **Fraud Rate**: 0.17% of transactions (industry average)
- **Average Fraud Loss**: $125 per incident
- **Transaction Volume**: ~1 million transactions/day

### 3.3 Success Criteria (How We Win)
1. **Detection Rate (Recall)**: Catch >90% of fraud
2. **Precision**: <2% false positive rate (98% precision)
3. **Speed**: <100ms prediction latency
4. **Cost Savings**: Reduce fraud losses by 70%+
5. **Explainability**: Provide top 3 reasons for each fraud flag

---

## 4. TECHNICAL APPROACH

### 4.1 Machine Learning Strategy
**Supervised Learning** using historical labeled transactions

**Why Supervised Learning?**
- We have historical data with fraud labels
- Clear input-output relationship
- Proven approach for classification

**Alternatives Considered:**
- Unsupervised (Anomaly Detection): No labels needed, but less accurate
- Semi-supervised: Useful when labels are scarce (not our case)
- Rule-based: Interpretable but rigid and easy to evade

### 4.2 Model Selection Criteria
Models must be:
- **Fast**: Inference <50ms
- **Interpretable**: SHAP values, feature importance
- **Robust**: Handle imbalanced data
- **Production-ready**: Easy to deploy and monitor

**Candidate Models:**
1. Logistic Regression (baseline)
2. Random Forest (ensemble, interpretable)
3. XGBoost (high performance, industry standard)
4. LightGBM (faster than XGBoost)
5. Neural Network (if needed, but adds complexity)

### 4.3 Handling Class Imbalance
**Challenge**: Only 0.17% of transactions are fraud

**Solutions to Apply:**
1. **Resampling**: SMOTE (Synthetic Minority Oversampling)
2. **Class Weights**: Penalize fraud misclassification more
3. **Evaluation Metrics**: Precision-Recall instead of Accuracy
4. **Threshold Tuning**: Adjust decision boundary

---

## 5. DATA UNDERSTANDING

### 5.1 Dataset
**Source**: Kaggle Credit Card Fraud Detection Dataset
- **Size**: 284,807 transactions
- **Features**: 31 (Time, Amount, V1-V28, Class)
- **Fraud Rate**: 0.172% (492 frauds)
- **Time Period**: 2 days of European cardholders

### 5.2 Feature Description
| Feature | Type | Description |
|---------|------|-------------|
| Time | Numerical | Seconds elapsed from first transaction |
| V1-V28 | Numerical | PCA-transformed features (confidential) |
| Amount | Numerical | Transaction amount |
| Class | Binary | 0=Legitimate, 1=Fraud |

**Why PCA Features?**
- Protect customer privacy (no raw names, addresses, card numbers)
- Already dimensionality-reduced
- Industry standard for shared datasets

### 5.3 Data Challenges
1. **Extreme Imbalance**: 0.17% fraud rate
2. **Anonymized Features**: Can't engineer domain-specific features
3. **Limited Time Range**: Only 2 days (may not capture all patterns)
4. **No Missing Values**: Clean dataset (unusual in real-world)

---

## 6. EVALUATION STRATEGY

### 6.1 Why NOT Accuracy?
**Example:**
- Dataset: 99.83% legitimate, 0.17% fraud
- A model predicting "legitimate" 100% of time gets 99.83% accuracy
- But catches ZERO fraud! ❌

### 6.2 Primary Metrics

#### Confusion Matrix
```
                    Predicted
                Legitimate  Fraud
Actual Legit    TN          FP
       Fraud    FN          TP
```

#### Key Metrics
1. **Precision = TP / (TP + FP)**
   - "Of flagged transactions, how many are actually fraud?"
   - Target: >98% (minimize false alarms)

2. **Recall = TP / (TP + FN)**
   - "Of all fraud, how much did we catch?"
   - Target: >90% (catch most fraud)

3. **F1-Score = 2 × (Precision × Recall) / (Precision + Recall)**
   - Harmonic mean, balances both
   - Target: >0.85

4. **PR-AUC (Precision-Recall Area Under Curve)**
   - Better than ROC-AUC for imbalanced data
   - Target: >0.90

5. **Matthews Correlation Coefficient (MCC)**
   - Considers all confusion matrix values
   - Range: -1 to +1 (higher is better)
   - Target: >0.80

### 6.3 Business Metrics
- **Cost per Transaction**: (FN × $125) + (FP × $20)
- **Fraud Loss Reduction**: % decrease in fraud losses
- **Customer Friction**: Number of blocked legitimate transactions

---

## 7. DEPLOYMENT REQUIREMENTS

### 7.1 Production Environment
- **Platform**: AWS (S3, Lambda, API Gateway)
- **API Type**: RESTful API
- **Format**: JSON input/output
- **SLA**: 99.9% uptime, <100ms latency

### 7.2 API Specification
**Endpoint**: `POST /predict`

**Request:**
```json
{
  "transaction_id": "txn_123456",
  "time": 12345,
  "amount": 149.99,
  "v1": -1.359807,
  "v2": -0.072781,
  ...
  "v28": 0.014207
}
```

**Response:**
```json
{
  "transaction_id": "txn_123456",
  "prediction": "fraud",
  "fraud_probability": 0.94,
  "risk_score": "high",
  "top_reasons": [
    "Unusual transaction amount",
    "Suspicious time pattern",
    "High V14 value"
  ],
  "action": "block"
}
```

### 7.3 Monitoring
- **Model Drift**: Track feature distributions weekly
- **Performance Degradation**: Monitor Precision/Recall daily
- **Latency**: Alert if >100ms
- **Error Rate**: Alert if >1%

---

## 8. PROJECT CONSTRAINTS

### 8.1 Technical Constraints
- ✅ **Budget**: $0 (AWS Free Tier only)
- ✅ **Timeline**: 6 weeks part-time
- ✅ **Compute**: No GPU required (tabular data)
- ✅ **Storage**: <5GB (within S3 free tier)

### 8.2 AWS Free Tier Limits
- **S3**: 5GB storage, 20,000 GET requests, 2,000 PUT requests/month
- **Lambda**: 1M requests/month, 400,000 GB-seconds compute
- **EC2**: 750 hours/month t2.micro or t3.micro
- **SageMaker**: 250 hours/month ml.t3.medium notebooks

### 8.3 Compliance & Ethics
- **No PII Storage**: All features anonymized
- **Explainability**: Required for blocked transactions
- **Bias Testing**: Ensure no demographic discrimination
- **Audit Trail**: Log all predictions for review

---

## 9. RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Model overfits to 2-day dataset | High | Medium | Cross-validation, regularization |
| Fraudsters adapt to model | High | High | Regular retraining (monthly) |
| AWS Free Tier exceeded | Medium | Low | Monitor usage, set billing alerts |
| High false positive rate | High | Medium | Threshold tuning, ensemble methods |
| Latency >100ms | Medium | Low | Model optimization, caching |

---

## 10. SUCCESS DEFINITION

### Minimum Viable Product (MVP)
- ✅ Achieves >85% Recall, >95% Precision
- ✅ Deploys on AWS with REST API
- ✅ Responds in <200ms
- ✅ Provides basic explainability

### Stretch Goals
- 🎯 >90% Recall, >98% Precision
- 🎯 <100ms latency
- 🎯 SHAP-based detailed explanations
- 🎯 Real-time monitoring dashboard
- 🎯 Automated retraining pipeline

---

## 11. NEXT STEPS
1. ✅ **Phase 1.1**: Problem definition (this document)
2. ⏭️ **Phase 1.2**: Environment setup (AWS, Python, Git)
3. ⏭️ **Phase 1.3**: Architecture design
4. ⏭️ **Phase 2**: Data acquisition and EDA

---

## INTERVIEW QUESTIONS YOU CAN NOW ANSWER

### Q1: "Why is fraud detection challenging?"
**Answer**: "Fraud detection faces three main challenges. First, extreme class imbalance—only 0.17% of transactions are fraudulent, making accuracy a misleading metric. Second, asymmetric costs where missing fraud costs $50-$5000 but false alarms only cost ~$20 in customer friction. Third, real-time requirements—we need predictions in under 100ms during transaction processing. Additionally, fraudsters constantly evolve their tactics, requiring regular model updates."

### Q2: "Why not use accuracy as your metric?"
**Answer**: "Accuracy is misleading for imbalanced datasets. In our case, a model that always predicts 'legitimate' would achieve 99.83% accuracy while catching zero fraud. Instead, we use Precision-Recall metrics, F1-score, and PR-AUC which better reflect performance on the minority class. We also calculate Matthews Correlation Coefficient which considers all four confusion matrix values."

### Q3: "How do you handle the class imbalance?"
**Answer**: "We use a multi-pronged approach: First, resampling techniques like SMOTE to synthetically balance the training set. Second, class weights to penalize fraud misclassification more heavily. Third, we use appropriate evaluation metrics like Precision-Recall curves instead of ROC curves. Finally, we tune the decision threshold based on business costs rather than using the default 0.5."

### Q4: "What's the business impact of your model?"
**Answer**: "Our model targets 90% fraud detection (Recall) with 98% precision, which would reduce fraud losses by approximately 70-85%. At 1 million transactions per day with 0.17% fraud rate and $125 average fraud loss, that translates to preventing ~$40,000 in daily fraud losses while keeping false alarms under 2%, maintaining customer satisfaction."

### Q5: "Why machine learning over rule-based systems?"
**Answer**: "Rule-based systems are rigid and easy for fraudsters to reverse-engineer and evade. ML models learn complex, non-linear patterns from data and adapt through retraining. However, we combine both: ML for pattern detection with explainability features that generate human-understandable reasons, giving us the best of both worlds—adaptive learning with interpretability."

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Author**: [Your Name]  
**Project**: Credit Card Fraud Detection System
