## Model Evaluation Report

### Overview

RUN_ID = `848720529722480596b667cae3a185a0`

| Metric | Value |
|-----------|-------|
| PR-AUC | 0.7998 |
| ROC-AUC | 0.9900 |

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Non-fraud (0) | 0.9998 | 0.9964 | 0.9981 | 1,688,906 |
| Fraud (1) | 0.2630 | 0.8540 | 0.4021 | 2,562 |
| Macro avg | 0.6314 | 0.9252 | 0.7001 | 1,691,468 |
| Weighted avg | 0.9987 | 0.9962 | 0.9972 | 1,691,468 |

### Performance Analysis

The model was evaluated on a test set of **1.691.468 transactions**, of which **2.562 were fraudulent** (~0,15% fraud rate). The **PR-AUC of ~0.8** is the more meaningful metric, and represents a decent result considering the extreme class imbalance and limited tuning:
- **Recall of 0.854** on the fraud class means the model detects 85.4% of all fraudulent transactions in the test set.
- **Precision of 0.263** on the fraud class means only 1 in 4 flagged transactions is actually fraudulent.
- **ROC-AUC of 0.99** is misleading in this context due to class imbalance — precision, recall and PR-AUC are the meaningful indicators.

### Real-World Considerations

At production scale, a recall of 85.4% still leaves a meaningful number of fraudulent transactions undetected, while a precision of 26.3% generates significant friction for legitimate customers. These limitations are understandable given the synthetic nature of the dataset and the scope of this project, and several avenues exist to improve them — including threshold tuning, cost-sensitive learning, and richer feature engineering. That said, defining the right targets is ultimately a business decision that requires alignment with fraud experts, risk managers, and stakeholders before further model iteration.