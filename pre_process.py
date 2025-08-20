import pandas as pd
import re
import uuid
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# ---------- SETUP ----------
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

male_file = "C:/Users/MSI/Downloads/merged_male_responses.csv"
female_file = "C:/Users/MSI/Downloads/merged_female_responses.csv"
output_file = "all_responses_clean.csv"

# ---------- LOAD & ADD GENDER ----------
df_male = pd.read_csv(male_file)
df_male["Gender"] = "male"

df_female = pd.read_csv(female_file)
df_female["Gender"] = "female"

# Merge
df = pd.concat([df_male, df_female], ignore_index=True)

# ---------- CLEAN FUNCTION ----------
def clean_text(text):
    if pd.isna(text):
        return ""
    
    # lowercase
    text = text.lower()
    
    # remove ads/disclaimers (example: lines starting with "note:", "disclaimer:", etc.)
    text = re.sub(r"(disclaimer:.*|note:.*|advertisement:.*)", "", text)
    
    # remove duplicate sentences
    sentences = list(dict.fromkeys(re.split(r'(?<=[.!?]) +', text)))
    text = " ".join(sentences)
    
    # remove special characters except punctuation
    text = re.sub(r"[^a-z0-9.,!?;:()'\" ]+", " ", text)
    
    # collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

# ---------- APPLY CLEAN ----------
df["Response_Clean"] = df["response"].apply(clean_text)

# ---------- ADD UNIQUE ID ----------
df.insert(0, "ID", [str(uuid.uuid4())[:8] for _ in range(len(df))])

# ---------- AUTO SENTIMENT ----------
def get_sentiment(text):
    if not text.strip():
        return "Neutral"
    
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Response_Clean"].apply(get_sentiment)

# ---------- ADD EMPTY SCORECARD COLUMNS ----------
df["Empathy"] = None           # scale 1–5
df["AdviceQuality"] = None     # scale 1–5
df["GenderedLang"] = None      # 0 / 1

# ---------- SAVE ----------
df.to_csv(output_file, index=False)

print(f"✅ Preprocessing + Sentiment done! File saved as {output_file}")
