import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1️⃣ Load your synthetic dataset
df = pd.read_csv("data/synthetic_churn_dataset.csv")

# 2️⃣ Define features & target
features = [
    "last_login_days", "usage_score", "tickets_last_30d", "avg_ticket_sentiment",
    "email_open_rate", "feature_drop_count", "payment_delay_days"
]
X = df[features]
y = df["churned"]

# 3️⃣ Scale features (XGBoost doesn't require scaling, but it helps with interpretation)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4️⃣ Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, stratify=y, random_state=42
)

# 5️⃣ Initialize your XGBoost churn model
model = XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=3,  # useful if churn is rare in real data
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# 6️⃣ Train model
model.fit(X_train, y_train)

# 7️⃣ Evaluate performance
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n🔎 Classification Report:")
print(classification_report(y_test, y_pred))

roc_score = roc_auc_score(y_test, y_proba)
print(f"\n🔵 ROC AUC: {roc_score:.3f}")

# 8️⃣ Save model + scaler
joblib.dump(model, "models/xgboost_churn_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("\n✅ XGBoost churn model and scaler saved in 'models/' directory.")
