# Success Metrics Framework
## Credit Card Fraud Detection System

---

## 1. METRICS HIERARCHY

### 1.1 Primary Business Metrics (What Executives Care About)
These translate technical performance to business value:

| Metric | Target | Formula | Business Impact |
|--------|--------|---------|-----------------|
| **Fraud Loss Reduction** | 70-85% | (Baseline Losses - New Losses) / Baseline Losses | Direct revenue protection |
| **False Positive Rate** | <2% | FP / (FP + TN) | Customer satisfaction |
| **Cost per Transaction** | <$0.50 | (FN × $125 + FP × $20) / Total Transactions | Operational efficiency |
| **ROI** | >500% | (Fraud Prevented - System Cost) / System Cost | Investment justification |

### 1.2 Primary ML Metrics (What Data Scientists Care About)
These measure model quality:

| Metric | Target | Why This Metric | When to Use |
|--------|--------|-----------------|-------------|
| **Precision** | >98% | "Are flagged transactions actually fraud?" | Minimize false alarms |
| **Recall** | >90% | "Are we catching most fraud?" | Maximize fraud detection |
| **F1-Score** | >0.85 | Harmonic mean of Precision & Recall | Balanced performance |
| **PR-AUC** | >0.90 | Overall discrimination ability | Model comparison |
| **MCC** | >0.80 | Correlation considering all classes | Imbalanced data |

### 1.3 Operational Metrics (What Engineers Care About)
These measure system performance:

| Metric | Target | Why Important |
|--------|--------|---------------|
| **Latency (p50)** | <50ms | Median user experience |
| **Latency (p95)** | <100ms | 95% of requests |
| **Latency (p99)** | <200ms | Worst case handling |
| **Throughput** | >1000 req/sec | Handle peak traffic |
| **Availability** | 99.9% | System reliability |
| **Error Rate** | <0.1% | Failure rate |

---

## 2. DETAILED METRIC DEFINITIONS

### 2.1 Confusion Matrix Foundation

```
                    PREDICTED
                Legitimate    Fraud
ACTUAL  Legit   TN (True      FP (False
                Negative)     Positive)
                
        Fraud   FN (False     TP (True
                Negative)     Positive)
```

**Definitions:**
- **TP (True Positive)**: Correctly identified fraud
- **TN (True Negative)**: Correctly identified legitimate
- **FP (False Positive)**: Legitimate flagged as fraud (Type I Error)
- **FN (False Negative)**: Fraud missed (Type II Error)

**Example with 10,000 transactions:**
- 9,983 Legitimate, 17 Fraud (0.17% fraud rate)
- Model catches 15 fraud (TP=15, FN=2)
- Model flags 50 legitimate as fraud (FP=50, TN=9,933)

```
Confusion Matrix:
              Predicted Legit  Predicted Fraud
Actual Legit      9,933            50
Actual Fraud         2             15
```

---

### 2.2 PRECISION (Positive Predictive Value)

**Formula:**
```
Precision = TP / (TP + FP)
          = True Fraud / All Flagged Transactions
```

**Example:**
```
Precision = 15 / (15 + 50) = 15 / 65 = 0.231 = 23.1%
```

**Interpretation:**
"Of all transactions we flagged as fraud, only 23.1% were actually fraudulent."

**Why It Matters:**
- High Precision = Few false alarms
- Low Precision = Many legitimate transactions blocked
- **Customer Impact**: Frustrated customers, abandoned carts

**Target: >98%**
- At least 98 out of 100 flagged transactions are real fraud
- Maximum 2 false alarms per 100 flags

**Interview Answer:**
"Precision measures how accurate our fraud flags are. In production, low precision causes customer friction—imagine blocking someone's legitimate $500 grocery purchase. We target 98% precision to maintain trust while catching fraud."

---

### 2.3 RECALL (Sensitivity, True Positive Rate)

**Formula:**
```
Recall = TP / (TP + FN)
       = True Fraud / All Actual Fraud
```

**Example:**
```
Recall = 15 / (15 + 2) = 15 / 17 = 0.882 = 88.2%
```

**Interpretation:**
"We caught 88.2% of all fraud, but missed 11.8%."

**Why It Matters:**
- High Recall = Catch most fraud
- Low Recall = Letting fraud slip through
- **Business Impact**: Direct financial losses

**Target: >90%**
- Catch at least 90 out of 100 fraudulent transactions
- Miss maximum 10% of fraud

**Interview Answer:**
"Recall measures what percentage of fraud we detect. At 90% recall, we catch 9 out of 10 fraudulent transactions, significantly reducing financial losses. The missed 10% might be sophisticated attacks that require human review."

---

### 2.4 F1-SCORE (Harmonic Mean)

**Formula:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Example:**
```
F1 = 2 × (0.231 × 0.882) / (0.231 + 0.882)
   = 2 × 0.204 / 1.113
   = 0.366
```

**Why Harmonic Mean?**
- Arithmetic mean (Precision + Recall) / 2 doesn't penalize extremes
- Harmonic mean forces balance
- Example: Precision=1.0, Recall=0.1
  - Arithmetic mean = 0.55 (looks okay)
  - Harmonic mean = 0.18 (reveals problem)

**Interpretation:**
- F1 close to 1.0 = Both Precision and Recall are high
- F1 close to 0.0 = At least one metric is very low

**Target: >0.85**

**Interview Answer:**
"F1-score balances Precision and Recall using harmonic mean, which is stricter than arithmetic mean. It's useful when we care equally about false alarms and missed fraud. However, in fraud detection, we often weight Recall higher, so I also report metrics separately."

---

### 2.5 PR-AUC (Precision-Recall Area Under Curve)

**What It Measures:**
Area under the curve when plotting Precision (y-axis) vs Recall (x-axis) at different thresholds.

**Why Better Than ROC-AUC for Imbalanced Data:**

**ROC Curve (Not Ideal):**
- Plots: True Positive Rate vs False Positive Rate
- Problem: FPR = FP / (FP + TN)
- With 99.83% legitimate transactions, TN is HUGE
- A few false positives barely move FPR
- **Result**: ROC-AUC looks great even for bad models!

**PR Curve (Better):**
- Plots: Precision vs Recall
- Precision = TP / (TP + FP) focuses on positives only
- More sensitive to minority class performance
- **Result**: Honest picture of fraud detection ability

**Target: >0.90**

**Example:**
```python
# Threshold  Precision  Recall
# 0.9        0.99       0.50
# 0.7        0.95       0.75
# 0.5        0.90       0.85
# 0.3        0.80       0.92
# 0.1        0.60       0.98
```

**Interview Answer:**
"For imbalanced datasets, PR-AUC is superior to ROC-AUC. With 99.83% legitimate transactions, ROC-AUC can look high even for mediocre models because the huge number of true negatives makes FPR look low. PR-AUC focuses on the minority class, giving us an honest assessment."

---

### 2.6 MATTHEWS CORRELATION COEFFICIENT (MCC)

**Formula:**
```
MCC = (TP × TN - FP × FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))
```

**Range:** -1 to +1
- +1 = Perfect prediction
- 0 = Random guessing
- -1 = Perfect inverse prediction

**Why MCC?**
- Uses ALL four confusion matrix values
- Not biased by class imbalance
- Symmetric (treats both classes equally)

**Example:**
```
TP=15, FP=50, FN=2, TN=9,933

MCC = (15×9,933 - 50×2) / sqrt((15+50)(15+2)(9,933+50)(9,933+2))
    = (148,995 - 100) / sqrt(65 × 17 × 9,983 × 9,935)
    = 148,895 / sqrt(110,000,000,000)
    = 148,895 / 331,662
    = 0.449
```

**Interpretation:**
MCC of 0.449 indicates moderate positive correlation (better than random).

**Target: >0.80**

**Interview Answer:**
"MCC is the most informative metric for imbalanced classification because it considers all four confusion matrix values. Unlike Precision or Recall which can be artificially high by predicting only one class, MCC requires balance across both classes."

---

### 2.7 COST-BASED METRICS

**Business Reality:**
Not all errors cost the same!

**Cost Matrix:**
```
                Predicted Legit   Predicted Fraud
Actual Legit         $0               $20
                  (Correct)      (False alarm,
                                customer friction)

Actual Fraud       $125              $0
                (Missed fraud,    (Caught fraud)
                 financial loss)
```

**Total Cost Formula:**
```
Total Cost = (FN × $125) + (FP × $20)
```

**Example:**
```
Total Cost = (2 × $125) + (50 × $20)
           = $250 + $1,000
           = $1,250 for 10,000 transactions
           = $0.125 per transaction
```

**Cost per Day (1M transactions):**
```
Cost = $0.125 × 1,000,000 = $125,000/day
```

**Baseline (No Model):**
```
All fraud goes through: 1,700 frauds × $125 = $212,500/day
Savings = $212,500 - $125,000 = $87,500/day
```

**Target: <$0.50 per transaction**

**Interview Answer:**
"We optimize for business cost, not just accuracy. Missing a fraud costs $125 in losses, while a false alarm costs $20 in customer friction. Our model's threshold is tuned to minimize total cost: (False Negatives × $125) + (False Positives × $20)."

---

## 3. THRESHOLD TUNING

**Default Threshold Problem:**
Most models use 0.5 by default, but this isn't optimal for imbalanced or cost-sensitive problems.

**How to Find Optimal Threshold:**

### Method 1: Cost-Based
```python
def find_optimal_threshold(y_true, y_pred_proba, cost_fn=125, cost_fp=20):
    thresholds = np.arange(0.01, 0.99, 0.01)
    costs = []
    
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        
        total_cost = (fn * cost_fn) + (fp * cost_fp)
        costs.append(total_cost)
    
    optimal_threshold = thresholds[np.argmin(costs)]
    return optimal_threshold
```

### Method 2: F1-Based
```python
def find_f1_optimal_threshold(y_true, y_pred_proba):
    thresholds = np.arange(0.01, 0.99, 0.01)
    f1_scores = []
    
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        f1 = f1_score(y_true, y_pred)
        f1_scores.append(f1)
    
    optimal_threshold = thresholds[np.argmax(f1_scores)]
    return optimal_threshold
```

### Method 3: Business Constraint
"We MUST catch 90% of fraud, what's the minimum false positive rate?"
```python
def find_threshold_for_recall(y_true, y_pred_proba, target_recall=0.90):
    thresholds = np.arange(0.01, 0.99, 0.01)
    
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        recall = recall_score(y_true, y_pred)
        
        if recall >= target_recall:
            precision = precision_score(y_true, y_pred)
            return threshold, precision, recall
```

**Interview Answer:**
"We don't use the default 0.5 threshold. Instead, we tune it based on business costs. By plotting total cost against thresholds from 0.01 to 0.99, we find the threshold that minimizes (False Negatives × $125) + (False Positives × $20). This often results in a lower threshold like 0.3, prioritizing fraud detection."

---

## 4. METRICS TRACKING PLAN

### 4.1 During Development
**Track Weekly:**
- Model performance on validation set
- Training time per model
- Feature importance changes

### 4.2 After Deployment
**Track Daily:**
- Precision, Recall, F1-Score on production data
- Latency (p50, p95, p99)
- Error rate
- Cost per transaction

**Track Weekly:**
- Feature distribution drift
- Prediction distribution (% flagged as fraud)
- User feedback (disputed flags)

**Track Monthly:**
- Model retrain and compare metrics
- A/B test results (new model vs old)

---

## 5. REPORTING TEMPLATE

### Executive Dashboard (1-Page)
```
┌──────────────────────────────────────────────────┐
│  FRAUD DETECTION PERFORMANCE - April 2026        │
├──────────────────────────────────────────────────┤
│                                                  │
│  💰 Fraud Losses Prevented: $87,500/day         │
│  📊 Detection Rate: 88.2% of fraud caught       │
│  ✅ False Alarm Rate: 0.5%                      │
│  ⚡ System Latency: 47ms average               │
│                                                  │
│  🎯 Status: Meeting Targets ✓                   │
└──────────────────────────────────────────────────┘
```

### Technical Report
```
Model Performance Summary
========================
Dataset: 284,807 transactions (492 fraud, 0.17%)
Train/Val/Test Split: 70/15/15

Metrics on Test Set:
--------------------
Precision:          98.2%
Recall:             88.2%
F1-Score:           0.929
PR-AUC:             0.952
MCC:                0.893

Confusion Matrix:
                Predicted
            Legit    Fraud
Actual Legit  42,627    85
       Fraud      6     65

Business Impact:
----------------
Cost per Transaction: $0.32
Daily Savings: $87,500
False Positive Rate: 0.20%
False Negative Rate: 8.45%

Operational:
------------
Avg Latency: 47ms
P95 Latency: 89ms
Throughput: 1,247 req/sec
```

---

## INTERVIEW QUESTIONS YOU CAN NOW ANSWER

### Q1: "Walk me through your evaluation metrics."
**Answer**: "I use a hierarchy of metrics. For business stakeholders, I report fraud loss reduction (targeting 70-85%) and cost per transaction (<$0.50). For technical evaluation, I focus on Precision (>98% to minimize false alarms), Recall (>90% to catch most fraud), and F1-Score (>0.85 for balance). I prefer PR-AUC over ROC-AUC because with 99.83% legitimate transactions, ROC-AUC can be misleadingly high. Finally, I calculate Matthews Correlation Coefficient as it's unbiased for imbalanced data."

### Q2: "Why is accuracy a poor metric here?"
**Answer**: "Accuracy is the ratio of correct predictions to total predictions. In our case, a naive model that always predicts 'legitimate' would achieve 99.83% accuracy since 99.83% of transactions are legitimate. But this model would have 0% Recall—it wouldn't catch any fraud at all. That's why we use Precision-Recall metrics that focus on the minority class performance."

### Q3: "How do you tune your decision threshold?"
**Answer**: "I don't use the default 0.5 threshold. Instead, I create a cost function: Total Cost = (False Negatives × $125) + (False Positives × $20), reflecting that missed fraud costs more than false alarms. I plot this cost across thresholds from 0.01 to 0.99 and select the threshold that minimizes total cost. This often results in a lower threshold like 0.3, biasing toward catching fraud even if it increases false positives slightly."

### Q4: "What's the trade-off between Precision and Recall?"
**Answer**: "There's an inverse relationship. Lowering the threshold increases Recall (we catch more fraud) but decreases Precision (more false alarms). Raising it does the opposite. The optimal point depends on business priorities. In fraud detection, we typically prioritize Recall because missing a $1000 fraud is worse than blocking one legitimate $20 transaction. We tune the threshold to achieve our target Recall (90%), then optimize Precision from there."

### Q5: "How would you present model performance to non-technical stakeholders?"
**Answer**: "I translate metrics to business impact. Instead of 'Our model achieved 88.2% Recall and 98.2% Precision,' I say: 'Our system prevents $87,500 in daily fraud losses while only flagging 0.5% of legitimate transactions for review—that's just 1 false alarm per 200 transactions.' I also show a simple dashboard with dollars saved, detection rate, and customer friction metrics."

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Project**: Credit Card Fraud Detection System
