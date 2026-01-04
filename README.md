# 🔐 Phishing Website Detection

A simple machine learning–based system that detects whether a URL is **Phishing** or **Legitimate** using **URL structure analysis**.

## 📌 About the Project

This project analyzes the **lexical features of a URL** (length, characters, randomness, HTTPS usage, etc.) to identify phishing websites.
It does not rely on website content or third-party APIs, making it fast and lightweight.

The system is deployed as a **Streamlit web application** for real-time URL checking.

## ⚙️ How It Works

1. User enters a URL
2. URL features are extracted
3. A trained machine learning model classifies the URL
4. Result is shown with **Risk Level** and **Explanation**

Trusted domains (educational, government, and well-known platforms) are handled separately to reduce false positives.

## 🧠 Model Used

* **Random Forest Classifier**
* Accuracy: **~99.5%** (offline evaluation)
* Trained using URL-based lexical features

## 🛠️ Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit

# Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
# Note

This project performs **lexical URL analysis only** and does not check website reputation or content.
It is intended as a **learning and demonstration project**.

# Author
Hithaishi S P