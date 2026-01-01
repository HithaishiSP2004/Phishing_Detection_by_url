import pandas as pd

# Read only the URL column safely
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

# Rename column to standard format
phishing.rename(columns={"URL": "url"}, inplace=True)
benign.rename(columns={"URL": "url"}, inplace=True)

# Add labels
phishing["label"] = 1
benign["label"] = 0

# Combine & shuffle
df = pd.concat([phishing, benign], ignore_index=True)
df = df.sample(frac=1, random_state=42)

# Save final dataset
df.to_csv("data/urls.csv", index=False)

print("Dataset prepared successfully!")
print(df.head())
print("Total rows:", len(df))
