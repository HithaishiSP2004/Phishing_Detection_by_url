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

# ---------------- Custom Styling ----------------
st.markdown("""
<style>
.main-title {
    font-size: 34px;
    font-weight: 700;
}
.sub-text {
    font-size: 16px;
    color: #cccccc;
}
.section-heading {
    font-size: 20px;
    font-weight: 600;
    margin-top: 25px;
}
.footer {
    margin-top: 60px;
    padding-top: 15px;
    border-top: 1px solid #444;
    font-size: 14px;
    text-align: center;
    color: #aaaaaa;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="main-title">Phishing Website Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">URL-based phishing detection using machine learning and lexical analysis.</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- About Section ----------------
with st.expander("About this detection system"):
    st.write(
        "This system performs lexical URL analysis only. "
        "It does not scan website content or check domain reputation. "
        "A limited trusted-domain allowlist is used to reduce false positives."
    )

st.markdown("**Model Accuracy (Offline Evaluation):** ~99.5%")

st.markdown("---")

# ---------------- Input ----------------
url = st.text_input("Enter URL", placeholder="https://example.com")

# ---------------- Trusted Domains ----------------
trusted_suffix_domains = (".edu", ".edu.in", ".gov", ".gov.in")

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
    if prediction == 1:
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
            reasons.append("URL structure matches learned phishing patterns")
    else:
        reasons.append("No strong phishing indicators detected")

    return reasons


# ---------------- Detection Logic ----------------
if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Trusted exact domains
        if domain in trusted_exact_domains:
            st.success("Legitimate URL (Trusted Platform)")
            st.markdown("**Risk Level:** Low Risk")

            st.markdown("### Detection Strength")
            st.progress(0.95)

            st.markdown("### Explanation")
            st.write("• Verified and widely trusted web platform")

        # Trusted suffix domains
        elif domain.endswith(trusted_suffix_domains):
            st.success("Legitimate URL (Trusted Domain)")
            st.markdown("**Risk Level:** Low Risk")

            st.markdown("### Detection Strength")
            st.progress(0.9)

            st.markdown("### Explanation")
            st.write("• Trusted educational or government domain")

        else:
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

            st.markdown("### Explanation")
            for r in explain_flags(features, pred):
                st.write(f"- {r}")

            st.markdown("### Extracted URL Features")
            st.dataframe(df.T, use_container_width=True)

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Phishing Website Detection System | Built using Python & Scikit-learn<br>
Developed by Hithaishi S P | Version 1.1
</div>
""", unsafe_allow_html=True)