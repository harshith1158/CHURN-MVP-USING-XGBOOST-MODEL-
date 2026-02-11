import joblib
import os
from google.cloud import bigquery

# 1️⃣ Load the production model & scaler
MODEL_PATH = os.path.join("models", "xgboost_churn_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except FileNotFoundError as e:
    print(f"❌ Model or scaler file not found: {e}")
    exit(1)

# Make sure you have set GOOGLE_APPLICATION_CREDENTIALS environment variable
client = bigquery.Client()

query = """
    SELECT
        last_login_days,
        usage_score,
        tickets_last_30d,
        avg_ticket_sentiment,
        email_open_rate,
        feature_drop_count,
        payment_delay_days
    FROM `your_project_id.synthetic_churn.synthetic_customer_usage`
"""
try:
    df = client.query(query).to_dataframe()
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}")
    exit(1)

# 3️⃣ Extract the same features used during training
features = [
    "last_login_days", "usage_score", "tickets_last_30d", "avg_ticket_sentiment",
    "email_open_rate", "feature_drop_count", "payment_delay_days"
]
X_new = df[features]

# 4️⃣ Scale new data
X_scaled = scaler.transform(X_new)

# 5️⃣ Predict churn probabilities & health scores
churn_probs = model.predict_proba(X_scaled)[:, 1]
df["churn_probability"] = churn_probs
df["health_score"] = (1 - churn_probs) * 100

# 6️⃣ Save predictions
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(DATA_DIR, "customer_churn_health_report.csv")
df.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Predictions complete! Results saved to {OUTPUT_PATH}")

# 7️⃣ Print a preview
print(df[["churn_probability", "health_score"]].head())
