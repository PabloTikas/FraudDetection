import mlflow
import mlflow.xgboost
from pathlib import Path
import pandas as pd

ARTIFACT_PATH = (Path(__file__).parent.parent / 'model' / 'artifacts').resolve(strict=True)

model = mlflow.xgboost.load_model(ARTIFACT_PATH)

FEATURE_ORDER = [
    'amount', 'use_chip', 'merchant_city', 'errors', 'current_age', 'gender',
    'latitude', 'longitude', 'per_capita_income', 'yearly_income', 'total_debt',
    'credit_score', 'num_credit_cards', 'card_brand', 'card_type', 'has_chip',
    'num_cards_issued', 'credit_limit', 'merchant_category', 'trans_count_cli',
    'avg_amount_cli', 'max_amount_cli', 'trans_count_card', 'hour', 'day_of_week',
    'month', 'day', 'days_since_acct_open', 'days_until_expiration',
    'years_since_pin_change', 'years_retired'
]

CAT_COLUMNS = ['use_chip', 'merchant_city', 'errors', 'gender', 'card_brand', 'card_type', 'has_chip', 'merchant_category']

def predict_pipeline(X) -> tuple[int, float]:
    pred_df = pd.DataFrame([X.model_dump()])[FEATURE_ORDER]

    for col in CAT_COLUMNS:
        pred_df[col] = pred_df[col].astype('category')

    y_pred = int(model.predict(pred_df)[0])
    y_prob = float(model.predict_proba(pred_df)[:,1][0])
    return y_pred, y_prob