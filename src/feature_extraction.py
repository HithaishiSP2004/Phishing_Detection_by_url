import re
from urllib.parse import urlparse
import math

def shannon_entropy(s):
    probs = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(url):
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)

    features["count_dot"] = url.count(".")
    features["count_hyphen"] = url.count("-")
    features["count_at"] = url.count("@")
    features["count_question"] = url.count("?")
    features["count_equal"] = url.count("=")
    features["count_slash"] = url.count("/")

    features["digit_count"] = sum(c.isdigit() for c in url)
    features["letter_count"] = sum(c.isalpha() for c in url)

    features["has_https"] = 1 if parsed.scheme == "https" else 0
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

    suspicious_words = [
        "login","verify","secure","account",
        "update","bank","free","bonus"
    ]
    features["suspicious_words"] = sum(
        word in url.lower() for word in suspicious_words
    )

    features["entropy"] = shannon_entropy(url)

    features["subdomain_count"] = domain.count(".")

    return features
