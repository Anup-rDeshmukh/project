import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# load data
df = pd.read_csv(r"D:/coding/project/sms_filtering/data/sms_data.csv")

print(df.head())

# drop invalid sms
df = df.dropna(subset=["text", "senderAddress"])
df = df[df["text"].str.strip() != ""]

# cleaning
def clean_sms(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z0-9₹.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_sms)

# expense filter
expense_keywords = [
    "spent", "debit", "purchase", "paid","paytm","phonepe","gpay","googlepay",
    "payment", "withdrawn", "dr", "txn"
]

def is_expense_sms(text):
    return any(word in text for word in expense_keywords)

df["is_expense"] = df["clean_text"].apply(is_expense_sms)
expense_df = df[df["is_expense"]].copy()

# amount extraction
def extract_amount(text):
    patterns = [
        r"(rs\.?|₹|inr)\s?([\d,]+(\.\d+)?)",
        r"([\d,]+(\.\d+)?)\s?(rs\.?|₹)"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            amount = match.group(2) if match.group(2) else match.group(1)
            return float(amount.replace(",", ""))
    return None

expense_df["amount"] = expense_df["clean_text"].apply(extract_amount)
expense_df = expense_df.dropna(subset=["amount"])

# categories
categories = {
    "food": ["swiggy", "zomato", "restaurant", "cafe"],
    "payment":["paytm","phonepe","paid","sent","debited","credited"],
    "travel": ["uber", "ola", "irctc", "metro", "rapido"],
    "shopping": ["amazon", "flipkart", "myntra"],
    "fuel": ["petrol", "diesel", "fuel"],
    "bill": ["electricity", "recharge", "bill", "broadband"]
}

def assign_category(text):
    for cat, keys in categories.items():
        if any(k in text for k in keys):
            return cat
    return "others"

expense_df["category"] = expense_df["clean_text"].apply(assign_category)

expense_df = expense_df[["clean_text", "amount", "category"]]

# vectorization
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
X = vectorizer.fit_transform(expense_df["clean_text"])
y = expense_df["category"]

# save
expense_df.to_csv("clean_expense_sms.csv", index=False)