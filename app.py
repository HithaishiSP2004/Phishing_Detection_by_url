import streamlit as st
import joblib
import pandas as pd
from src.feature_extraction import extract_features
from urllib.parse import urlparse

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Phishing Website Detection",
    layout="centered"
)

# ---------------- Load Model ----------------
model = joblib.load("model/phishing_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")

# ---------------- UI Header ----------------
st.title("Phishing Website Detection")
st.write("URL-based phishing detection using machine learning and lexical analysis.")

# Collapsible disclaimer (clean UI)
with st.expander("About this detection system"):
    st.write(
        "This system performs **lexical URL analysis only**. "
        "It does not verify website reputation, ownership, or webpage content. "
        "A limited trusted-domain allowlist is used to reduce false positives. "
        "Some legitimate websites may still be flagged due to structural similarities."
    )

# Static model info
st.markdown("**Model Accuracy:** ~99.5% (Random Forest Classifier)")

url = st.text_input("Enter URL", placeholder="https://example.com")

# ---------------- Trusted Domains ----------------
trusted_suffix_domains = (
    ".edu", ".edu.in", ".gov", ".gov.in"
)

trusted_exact_domains = {
    "google.com", "www.google.com",
    "youtube.com", "www.youtube.com",
    "gmail.com", "www.gmail.com",
    "github.com", "www.github.com",
    "amazon.com", "www.amazon.com",
    "facebook.com", "www.facebook.com",
    "instagram.com", "www.instagram.com",
    "linkedin.com", "www.linkedin.com",
    "microsoft.com", "www.microsoft.com",
    "geeksforgeeks.org", "www.geeksforgeeks.org",
    "coursera.org", "www.coursera.org",
    "udemy.com", "www.udemy.com",
    "wikipedia.org", "www.wikipedia.org",
    "hithaishi-sp-portfolio.netlify.app"
}

# ---------------- Helper Functions ----------------
def get_risk_label(prediction, strength):
    if prediction == 1:  # Phishing
        if strength >= 0.85:
            return "High Risk"
        elif strength >= 0.6:
            return "Medium Risk"
        else:
            return "Low Risk"
    else:
        return "Low Risk"


def explain_flags(features, prediction):
    reasons = []

    if prediction == 1:
        if features["has_https"] == 0:
            reasons.append("URL does not use HTTPS")

        if features["digit_count"] > 0:
            reasons.append("Digits detected in domain name")

        if features["entropy"] > 3.5:
            reasons.append("High randomness in URL structure")

        if features["count_slash"] > 4:
            reasons.append("Excessive URL path depth")

        if features["path_length"] > 20:
            reasons.append("Unusually long URL path")

        if features["subdomain_count"] > 2:
            reasons.append("Multiple subdomains detected")

        if not reasons:
            reasons.append(
                "URL structure closely matches phishing patterns learned by the model"
            )
    else:
        reasons.append("No strong phishing indicators detected")

    return reasons


# ---------------- Main Logic ----------------
if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # -------- Trusted Exact Domains --------
        if domain in trusted_exact_domains:
            st.success("Legitimate URL (Trusted Platform)")
            st.markdown("**Risk Level:** Low Risk")

            st.markdown("### Detection Strength")
            st.progress(0.95)

            st.markdown("### Why this URL was flagged")
            st.write("• Verified and widely trusted web platform")

            st.stop()

        # -------- Trusted Suffix Domains --------
        if domain.endswith(trusted_suffix_domains):
            st.success("Legitimate URL (Trusted Domain)")
            st.markdown("**Risk Level:** Low Risk")

            st.markdown("### Detection Strength")
            st.progress(0.9)

            st.markdown("### Why this URL was flagged")
            st.write("• Trusted educational or government domain")

            st.stop()

        # -------- ML-Based Detection --------
        features = extract_features(url)
        df = pd.DataFrame([features])
        df = df.reindex(columns=feature_names, fill_value=0)

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][pred]

        strength = min(prob, 0.99)
        risk = get_risk_label(pred, strength)

        if pred == 1:
            st.error(f"Phishing URL detected ({risk})")
        else:
            st.success(f"Legitimate URL ({risk})")

        st.markdown("### Detection Strength")
        st.progress(strength)

        st.markdown("### Why this URL was flagged")
        for r in explain_flags(features, pred):
            st.write(f"- {r}")

        st.markdown("### Extracted URL Features")
        st.dataframe(df.T, use_container_width=True)
