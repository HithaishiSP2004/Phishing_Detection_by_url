import streamlit as st
import joblib
import pandas as pd
from src.feature_extraction import extract_features

st.set_page_config(
    page_title="Phishing Website Detection",
    page_icon="🔐",
    layout="centered"
)

model = joblib.load("model/phishing_model.pkl")

st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight:600;
}
.result-box {
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 Phishing Website Detection")
st.write("Detect malicious URLs using Machine Learning & URL feature analysis.")

url = st.text_input("🔗 Enter URL", placeholder="https://example.com")

if st.button("🚨 Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        features = extract_features(url)
        df = pd.DataFrame([features])

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][pred]

        if pred == 1:
            st.error(f"⚠️ **Phishing URL Detected**  \nConfidence: `{prob:.2f}`")
        else:
            st.success(f"✅ **Legitimate URL**  \nConfidence: `{prob:.2f}`")

        st.markdown("### 🔍 Extracted Features")
        st.dataframe(df.T, use_container_width=True)
