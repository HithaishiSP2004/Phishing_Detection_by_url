import pandas as pd

phishing = pd.read_csv(
    "data/phishing.csv",
    usecols=["URL"],
    on_bad_lines="skip"
)

benign = pd.read_csv(
    "data/benign.csv",
    usecols=["URL"],
    on_bad_lines="skip"
)

phishing.rename(columns={"URL": "url"}, inplace=True)
benign.rename(columns={"URL": "url"}, inplace=True)

phishing["label"] = 1
benign["label"] = 0

df = pd.concat([phishing, benign], ignore_index=True)
df = df.sample(frac=1, random_state=42)

df.to_csv("data/urls.csv", index=False)

print("Dataset prepared successfully")
print(df.head())
print("Total rows:", len(df))
