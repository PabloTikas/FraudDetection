# frontend.py
import os
import gradio as gr
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ---------------------------------------------------------------------------
# Fetch valid categories from the API at startup
# ---------------------------------------------------------------------------
try:
    categories = requests.get(f"{API_URL}/categories", timeout=5).json()
except Exception as e:
    print(f"WARNING: could not fetch /categories ({e}). Dropdowns will be empty.")
    categories = {}

def cat(field):
    return sorted(categories.get(field, []))

FIELDS = [
    "amount", "use_chip", "merchant_city", "errors", "merchant_category",
    "hour", "day_of_week", "month", "day",
    "current_age", "gender", "latitude", "longitude",
    "per_capita_income", "yearly_income", "total_debt",
    "credit_score", "num_credit_cards", "trans_count_cli",
    "avg_amount_cli", "max_amount_cli", "years_retired",
    "card_brand", "card_type", "has_chip", "num_cards_issued",
    "credit_limit", "trans_count_card",
    "days_since_acct_open", "days_until_expiration", "years_since_pin_change",
]

# ---------------------------------------------------------------------------
# Output renderers
# ---------------------------------------------------------------------------
def result_html(decision: str, fraud_prob: float) -> str:
    """Render the colored verdict box + confidence bar."""
    if decision == "Fraud":
        confidence = fraud_prob
        color = "#dc2626"   # red-600
        bg = "#fee2e2"      # red-100
    else:
        confidence = 1 - fraud_prob
        color = "#16a34a"   # green-600
        bg = "#dcfce7"      # green-100

    pct = confidence * 100
    return f"""
    <div style="padding:28px;border-radius:14px;background:{bg};
                border:2px solid {color};text-align:center;
                font-family:system-ui,-apple-system,sans-serif;">
      <div style="font-size:40px;font-weight:800;color:{color};
                  letter-spacing:1px;margin-bottom:18px;">
        {decision.upper()}
      </div>
      <div style="font-size:15px;color:#374151;margin-bottom:10px;">
        Confidence in this verdict: <strong>{pct:.1f}%</strong>
      </div>
      <div style="background:#e5e7eb;border-radius:8px;height:18px;overflow:hidden;">
        <div style="background:{color};height:100%;width:{pct:.1f}%;
                    transition:width .3s ease;"></div>
      </div>
    </div>
    """


def message_html(msg: str, tone: str = "warn") -> str:
    palette = {
        "warn": ("#fef3c7", "#f59e0b", "#92400e"),
        "info": ("#f3f4f6", "#9ca3af", "#4b5563"),
    }[tone]
    bg, border, text = palette
    return f"""
    <div style="padding:20px;border-radius:12px;background:{bg};
                border:2px {'dashed' if tone=='info' else 'solid'} {border};
                color:{text};text-align:center;font-size:16px;
                font-family:system-ui,-apple-system,sans-serif;">
      {msg}
    </div>
    """


INITIAL_HTML = message_html("Submit a transaction to see the prediction", tone="info")

# ---------------------------------------------------------------------------
# Prediction function (talks to the API over HTTP)
# ---------------------------------------------------------------------------
def predict(*values):
    payload = dict(zip(FIELDS, values))
    try:
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        return message_html(f"API error: {e}", tone="warn")

    data = r.json()
    if data.get("error"):
        return message_html(f"Validation error: {data['error']}", tone="warn")

    return result_html(data["decision"], data["probability"])

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
with gr.Blocks(title="Fraud Detector") as demo:
    gr.Markdown("# Fraud Detector")

    output = gr.HTML(value=INITIAL_HTML)
    submit = gr.Button("Predict", variant="primary", size="lg")

    with gr.Tab("Transaction"):
        amount = gr.Number(
            label="Transaction amount ($)",
            info="How much money was charged in this transaction",
            minimum=0.01, value=50.0,
        )
        use_chip = gr.Dropdown(
            label="Card reading method",
            info="How the card was read at the point of sale (chip, swipe, online, etc.)",
            choices=cat("use_chip"),
        )
        merchant_city = gr.Dropdown(
            label="Merchant city",
            info="City where the merchant is located",
            choices=cat("merchant_city"),
        )
        errors = gr.Dropdown(
            label="Transaction errors",
            info="Any error flags raised during the transaction (or 'None')",
            choices=cat("errors"),
        )
        merchant_category = gr.Dropdown(
            label="Merchant category",
            info="Type of business (grocery, restaurant, online retail, etc.)",
            choices=cat("merchant_category"),
        )
        hour = gr.Slider(
            label="Hour of day",
            info="Hour the transaction occurred (0 = midnight, 23 = 11 PM)",
            minimum=0, maximum=23, step=1, value=12,
        )
        day_of_week = gr.Slider(
            label="Day of week",
            info="0 = Monday, 6 = Sunday",
            minimum=0, maximum=6, step=1, value=0,
        )
        month = gr.Slider(
            label="Month of year",
            info="1 = January, 12 = December",
            minimum=1, maximum=12, step=1, value=1,
        )
        day = gr.Slider(
            label="Day of month",
            info="Calendar day of the transaction",
            minimum=1, maximum=31, step=1, value=1,
        )

    with gr.Tab("Client"):
        current_age = gr.Number(
            label="Client age (years)",
            minimum=18, maximum=130, precision=0, value=30,
        )
        gender = gr.Dropdown(
            label="Client gender",
            choices=cat("gender"),
        )
        latitude = gr.Number(
            label="Client latitude",
            info="Geographic coordinate (−90 to 90)",
            minimum=-90, maximum=90, value=0.0,
        )
        longitude = gr.Number(
            label="Client longitude",
            info="Geographic coordinate (−180 to 180)",
            minimum=-180, maximum=180, value=0.0,
        )
        per_capita_income = gr.Number(
            label="Per capita income ($)",
            info="Income per person in the client's area",
            minimum=0, value=0,
        )
        yearly_income = gr.Number(
            label="Client's yearly income ($)",
            minimum=0, value=0,
        )
        total_debt = gr.Number(
            label="Client's total debt ($)",
            minimum=0, value=0,
        )
        credit_score = gr.Number(
            label="Credit score",
            info="FICO-style score, 1–999",
            minimum=1, maximum=999, precision=0, value=700,
        )
        num_credit_cards = gr.Number(
            label="Number of credit cards owned",
            minimum=1, precision=0, value=1,
        )
        trans_count_cli = gr.Number(
            label="Total historical transactions (client)",
            info="Number of transactions the client has made in the past",
            minimum=0, precision=0, value=0,
        )
        avg_amount_cli = gr.Number(
            label="Client's average transaction amount ($)",
            minimum=0, value=0,
        )
        max_amount_cli = gr.Number(
            label="Client's largest transaction amount ($)",
            minimum=0, value=0,
        )
        years_retired = gr.Number(
            label="Years since retirement",
            info="0 if the client is not retired",
            minimum=0, precision=0, value=0,
        )

    with gr.Tab("Card"):
        card_brand = gr.Dropdown(
            label="Card brand",
            info="Visa, Mastercard, Amex, Discover, etc.",
            choices=cat("card_brand"),
        )
        card_type = gr.Dropdown(
            label="Card type",
            info="Credit, debit, or prepaid",
            choices=cat("card_type"),
        )
        has_chip = gr.Dropdown(
            label="Card has EMV chip",
            choices=cat("has_chip"),
        )
        num_cards_issued = gr.Number(
            label="Cards issued on this account",
            info="How many physical cards the issuer has produced for this account",
            minimum=1, precision=0, value=1,
        )
        credit_limit = gr.Number(
            label="Card credit limit ($)",
            minimum=0.01, value=1000.0,
        )
        trans_count_card = gr.Number(
            label="Total historical transactions on this card",
            minimum=0, precision=0, value=0,
        )
        days_since_acct_open = gr.Number(
            label="Days since card account was opened",
            minimum=0, precision=0, value=0,
        )
        days_until_expiration = gr.Number(
            label="Days until card expires",
            minimum=0, precision=0, value=0,
        )
        years_since_pin_change = gr.Number(
            label="Years since last PIN change",
            minimum=0, precision=0, value=0,
        )

    inputs = [
        amount, use_chip, merchant_city, errors, merchant_category,
        hour, day_of_week, month, day,
        current_age, gender, latitude, longitude,
        per_capita_income, yearly_income, total_debt,
        credit_score, num_credit_cards, trans_count_cli,
        avg_amount_cli, max_amount_cli, years_retired,
        card_brand, card_type, has_chip, num_cards_issued,
        credit_limit, trans_count_card,
        days_since_acct_open, days_until_expiration, years_since_pin_change,
    ]
    submit.click(fn=predict, inputs=inputs, outputs=output)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)