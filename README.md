
# CHURN-MVP-USING-XGBOOST-MODEL

Streamlit dashboard that visualizes customer churn probabilities and health scores.

Quick start (local)

1. Create and activate a Python environment:

```bash
python -m venv .venv

.venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
```

2. Run the dashboard:

```bash
cd ChurnEngine
streamlit run dashboard/dashboard.py
```

Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. On https://share.streamlit.io click **New app**, choose your repo and branch `main`, and set the app file to `dashboard/dashboard.py`.
3. Ensure `requirements.txt` is present at the repo root so Streamlit Cloud installs dependencies.

Data
- The app loads `data/customer_churn_health_report.csv`. Commit small sample CSVs to `data/`, or load data from external storage (S3, GDrive, etc.). Use `st.secrets` for credentials.

Docker (optional)

Build and run the provided `Dockerfile`:

```bash
docker build -t churn-dashboard .
docker run -p 8501:8501 churn-dashboard
```
# ChurnEngine Dashboard

This repository contains a Streamlit dashboard visualizing customer churn predictions.

## Deploy to Streamlit Community Cloud
1. Ensure `requirements.txt` is present at the repository root (already included).
2. Commit and push your repo to GitHub.
3. On https://share.streamlit.io sign in with GitHub.
4. Click **New app** → select the repository and branch.
5. Set **App file** to `dashboard/dashboard.py` and click **Deploy**.

Notes:
- Small CSV data can be committed under `dashboard/data/` or `data/`. For large/private datasets, host externally and load via URL or credentials stored in Streamlit Secrets.
- Add credentials in Streamlit Cloud under *Settings → Secrets* and access via `st.secrets`.

## Local Docker deployment
Build and run locally using Docker:

```bash
docker build -t churn-dashboard .
docker run -p 8501:8501 churn-dashboard
```

The app will be available at `http://localhost:8501`.
