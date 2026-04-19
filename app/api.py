import json
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, FieldValidationInfo
from fastapi import FastAPI
from typing import Literal
from model.model import predict_pipeline


with open(Path(__file__).parent / 'valid_categories.json') as f:
    CATEGORIES = json.load(f)

VALID_CATEGORIES = {col: set(values) for col, values in CATEGORIES.items()}

class TransactionData(BaseModel):

    # Transaction data
    amount: float = Field(gt=0)
    use_chip: str
    merchant_city: str
    errors: str
    merchant_category: str
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)

    # Client data
    current_age: int = Field(ge=18, le=130)
    gender: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    per_capita_income: float = Field(ge=0)
    yearly_income: float = Field(ge=0)
    total_debt: float = Field(ge=0)
    credit_score: int = Field(gt=0, lt=1000)
    num_credit_cards: int = Field(ge=1)
    trans_count_cli: int = Field(ge=0)
    avg_amount_cli: float = Field(ge=0)
    max_amount_cli: float = Field(ge=0)
    years_retired: int = Field(ge=0)

    # Card data
    card_brand: str
    card_type: str
    has_chip: str
    num_cards_issued: int = Field(ge=1)
    credit_limit: float = Field(gt=0)
    trans_count_card: int = Field(ge=0)

    # Transaction + card
    days_since_acct_open: int = Field(ge=0)
    days_until_expiration: int = Field(ge=0)
    years_since_pin_change: int = Field(ge=0)

    @field_validator('use_chip', 'merchant_city', 'errors', 'gender', 'card_brand', 'card_type', 'has_chip', 'merchant_category')
    @classmethod
    def validate_categoricals(cls, v: str, info: FieldValidationInfo) -> str:
        """
        Validates that categorical fields contain only values seen during training.

        This single validator handles all categorical fields by leveraging the
        info.field_name attribute to dynamically look up the valid category set
        for each field from the VALID_CATEGORIES dictionary loaded at startup.

        Args:
            v (str): The input value provided by the user for the field being validated.
            info (FieldValidationInfo): Pydantic metadata object containing field
                information, used here to retrieve the field name dynamically.

        Returns:
            str: The original value unchanged if validation passes.

        Raises:
            ValueError: If the input value is not found in the set of valid
                categories for the corresponding field.
        """
        field_name = info.field_name
        if v not in VALID_CATEGORIES[field_name]:
            raise ValueError(f"Invalid {field_name}: '{v}'. Must be one of the valid categories.")
        return v


class PredictionOut(BaseModel):
    decision: Literal['Fraud', 'Not Fraud']
    probability: float = Field(ge=0, le=1)

from fastapi import FastAPI

app = FastAPI(
    title='Fraud Prediction System',
    description='System for predicting fraudulent card transactions',
    version='1.0.0'
)

# HEALTH CHECK
@app.get('/')
def root():
    return {'status': 'ok'}

prediction_decoder = {0: 'Not Fraud', 1: 'Fraud'}

@app.post('/predict')
def get_prediction(data: TransactionData):
    """
    Prediction endpoint.

    Args:
        data (TransactionData): Validated transaction data
    Returns:
        {
            "decision": "Fraud" / "Not Fraud" = str,
            "probability": float,
            "error": "Error message" = str
        }
    """
    try:
        y_pred, y_prob = predict_pipeline(data)
        return {
            "decision": prediction_decoder[y_pred],
            "probability": y_prob,
            "error": None
        }
    except Exception as e:
        return {
            "decision": None,
            "probability": None,
            "error": str(e)
        }
    

@app.get('/categories')
def get_categories():
    """
    Returns valid values for categorical features.
    """
    return VALID_CATEGORIES