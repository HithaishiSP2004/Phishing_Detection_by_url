import streamlit as st
import joblib
import pandas as pd
from src.feature_extraction import extract_features

st.set_page_config(
    page_title="Phishing Website Detection",
    layout="centered"
)

# Load model & feature names
model = joblib.load("model/phishing_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")

# Subtle styling (not flashy)
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
}
.block {
    padding: 16px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("Phishing Website Detection")
st.write("URL-based phishing detection using machine learning and lexical analysis.")

url = st.text_input("Enter URL", placeholder="https://example.com")

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        features = extract_features(url)

        df = pd.DataFrame([features])
        df = df.reindex(columns=feature_names, fill_value=0)

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][pred]

        if pred == 1:
            st.error(f"Phishing URL detected\nConfidence: {prob:.2f}")
        else:
            st.success(f"Legitimate URL\nConfidence: {prob:.2f}")

        st.markdown("### Extracted URL Features")
        st.dataframe(df.T, use_container_width=True)
