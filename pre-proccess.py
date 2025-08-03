import pandas as pd
from hazm import Normalizer, word_tokenize, Stemmer
import re
import os

# -------------------------------
# مسیر فایل‌ها
# -------------------------------
INPUT_FILE = "data/doctor_info.xlsx"
STOPWORDS_FILE = "data/stopwords-fa.txt"
OUTPUT_FILE = "output/processed_doctors_comments.xlsx"

# -------------------------------
# بارگذاری stopwords
# -------------------------------
with open(STOPWORDS_FILE, "r", encoding="utf-8") as f:
    stopwords = f.read().split()

# -------------------------------
# ابزارهای پردازش متن
# -------------------------------
normalizer = Normalizer()

# -------------------------------
# پیش‌پردازش کامل نظر
# -------------------------------
def preprocess_comment(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)  # حذف علائم
    text = re.sub(r'\d+', '', text)                   # حذف اعداد
    text = re.sub(r'(.)\1{2,}', r'\1', text)          # حذف کشیده‌ها
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords]
    return " ".join(tokens)

# -------------------------------
# پیش‌پردازش سبک تگ‌ها
# -------------------------------
def clean_tags(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s,]', '', text)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text.strip()

# -------------------------------
# پاکسازی سبک نام پزشک
# -------------------------------
def clean_name(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    return text.strip()

# -------------------------------
# پاکسازی سبک تخصص
# -------------------------------
def clean_specialty(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text.strip()

# -------------------------------
# خواندن فایل اکسل
# -------------------------------
df = pd.read_excel(INPUT_FILE)

# -------------------------------
# اعمال پیش‌پردازش روی ستون‌های فارسی
# -------------------------------
df['نظر پردازش‌شده'] = df['نظر'].apply(preprocess_comment)
df['تگ‌ها پاکسازی‌شده'] = df['تگ های کامنت'].apply(clean_tags)
df['نام پاکسازی‌شده'] = df['نام پزشک'].apply(clean_name)
df['تخصص پاکسازی‌شده'] = df['تخصص'].apply(clean_specialty)

# -------------------------------
# ذخیره خروجی
# -------------------------------
os.makedirs("output", exist_ok=True)
df.to_excel(OUTPUT_FILE, index=False)
print("✅ پیش‌پردازش با موفقیت انجام شد. فایل خروجی در مسیر 'output/' ذخیره شد.")
