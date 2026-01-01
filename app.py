import streamlit as st
import joblib
import pandas as pd
from src.feature_extraction import extract_features

st.set_page_config(
    page_title="Phishing Website Detection",
    layout="centered"
)

# Load model and feature names
model = joblib.load("model/phishing_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")

st.title("Phishing Website Detection")
st.write("URL-based phishing detection using machine learning and lexical analysis.")

url = st.text_input("Enter URL", placeholder="https://example.com")

def get_risk_label(confidence):
    if confidence >= 85:
        return "High Risk"
    elif confidence >= 60:
        return "Medium Risk"
    else:
        return "Low Risk"

def explain_flags(features):
    reasons = []

    if features["has_https"] == 0:
        reasons.append("URL does not use HTTPS")

    if features["digit_count"] > 0:
        reasons.append("Digits detected in domain name")

    if features["entropy"] > 4.0:
        reasons.append("High randomness in URL structure")

    if features["count_slash"] > 4:
        reasons.append("Excessive path depth")

    if features["path_length"] > 20:
        reasons.append("Unusually long URL path")

    if features["suspicious_words"] > 0:
        reasons.append("Contains phishing-related keywords")

    if not reasons:
        reasons.append("No strong phishing indicators detected")

    return reasons

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        # Feature extraction
        features = extract_features(url)
        df = pd.DataFrame([features])
        df = df.reindex(columns=feature_names, fill_value=0)

        # Prediction
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][pred]
        confidence = prob * 100

        # Risk label
        risk = get_risk_label(confidence)

        # Display result
        if pred == 1:
            st.error(f"Phishing URL detected\nConfidence: {confidence:.2f}% ({risk})")
        else:
            st.success(f"Legitimate URL\nConfidence: {confidence:.2f}% ({risk})")

        # Confidence bar
        st.markdown("### Confidence Level")
        st.progress(int(confidence))

        # Explanation
        st.markdown("### Why this URL was flagged")
        reasons = explain_flags(features)
        for r in reasons:
            st.write(f"- {r}")

        # Feature table
        st.markdown("### Extracted URL Features")
        st.dataframe(df.T, use_container_width=True)
