import pandas as pd
import joblib
from feature_extraction import extract_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load prepared dataset
df = pd.read_csv("data/urls.csv")

X = df["url"].apply(extract_features).apply(pd.Series)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    random_state=42
)

model.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

# ---------- FEATURE IMPORTANCE ----------
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Important Features:")
print(importance_df.head(10))
# --------------------------------------

# Save model & feature names
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(list(X.columns), "model/feature_names.pkl")

print("Model and feature names saved successfully")
