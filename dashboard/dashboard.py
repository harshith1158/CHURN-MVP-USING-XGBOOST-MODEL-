import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1️⃣ Load enriched churn predictions
DATA_PATH = os.path.join("data", "customer_churn_health_report.csv")

# Ensure the data directory exists
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Please check the path.")
    st.stop()

required_columns = {"churn_probability", "health_score"}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns: {required_columns - set(df.columns)}")
    st.stop()

# 2️⃣ Streamlit App Configuration
st.set_page_config(
    page_title="Dynamic Churn Dashboard",
    layout="wide"
)
st.title("🚦 Dynamic Customer Churn Prediction Dashboard")
st.markdown("This dashboard visualizes live churn probabilities and customer health scores.")

# 3️⃣ Show Metrics
avg_churn_prob = df["churn_probability"].mean()
avg_health = df["health_score"].mean()
st.metric("📉 Average Churn Probability", f"{avg_churn_prob:.2%}")
st.metric("💚 Average Health Score", f"{avg_health:.1f}")

# 4️⃣ Distribution Chart
fig1 = px.histogram(df, x="churn_probability", nbins=20, title="Churn Probability Distribution")
st.plotly_chart(fig1, use_container_width=True)

# 5️⃣ Scatter Plot: Health vs Last Login Days
if "last_login_days" in df.columns:
    fig2 = px.scatter(
        df,
        x="last_login_days",
        y="health_score",
        color="churn_probability",
        color_continuous_scale="RdYlGn_r",
        title="Health Score vs. Last Login Days",
        labels={"last_login_days": "Days Since Last Login", "health_score": "Health Score"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# 6️⃣ Table of Top At-Risk Customers
st.subheader("🚨 Top Customers at Risk of Churning")
top_risk = df.sort_values("churn_probability", ascending=False).head(10)
st.dataframe(top_risk)
