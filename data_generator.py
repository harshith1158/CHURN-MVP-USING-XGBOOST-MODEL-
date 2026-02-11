import numpy as np
import pandas as pd
from google.cloud import bigquery

def generate_synthetic_data(n_samples=1000, churn_rate=0.25):
    np.random.seed(np.random.randint(1_000_000))
    df = pd.DataFrame({
        "last_login_days": np.random.randint(0, 365, size=n_samples),
        "usage_score": np.random.uniform(0, 1, size=n_samples),
        "tickets_last_30d": np.random.poisson(3, size=n_samples),
        "avg_ticket_sentiment": np.random.uniform(-1, 1, size=n_samples),
        "email_open_rate": np.random.uniform(0, 1, size=n_samples),
        "feature_drop_count": np.random.poisson(2, size=n_samples),
        "payment_delay_days": np.random.randint(0, 30, size=n_samples),
    })
    # Simulate churn probability & assign churned label
    churn_prob = 0.5 * (df["last_login_days"] / 365) + 0.3 * (1 - df["usage_score"])
    churn_prob = np.clip(churn_prob, 0, 1)
    df["churned"] = np.random.binomial(1, churn_prob)
    return df

def upload_to_bigquery(df, table_id):
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"✅ Uploaded {len(df)} rows to {table_id}")

if __name__ == "__main__":
    df = generate_synthetic_data(1000)
    print("✅ Generated synthetic data preview:")
    print(df.head())
    df.to_csv("data/synthetic_churn_dataset.csv", index=False)
    print("✅ Saved to local CSV.")
    
    # Uncomment the line below if you want to upload directly to BigQuery on every generation:
    #upload_to_bigquery(df, "student-gpt-451313.synthetic_churn.synthetic_customer_usage")
