import pandas as pd
from hazm import Normalizer, word_tokenize, Stemmer
import re
import os


INPUT_FILE = "data/doctor_info.xlsx"
STOPWORDS_FILE = "data/stopwords-fa.txt"
OUTPUT_FILE = "output/processed_doctors_comments.xlsx"


with open(STOPWORDS_FILE, "r", encoding="utf-8") as f:
    stopwords = f.read().split()


normalizer = Normalizer()


def preprocess_comment(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)  
    text = re.sub(r'\d+', '', text)                   
    text = re.sub(r'(.)\1{2,}', r'\1', text)          
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords]
    return " ".join(tokens)


def clean_tags(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s,]', '', text)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text.strip()


def clean_name(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    return text.strip()


def clean_specialty(text):
    if pd.isna(text): return ""
    text = normalizer.normalize(str(text))
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text.strip()


df = pd.read_excel(INPUT_FILE)


df['نظر پردازش‌شده'] = df['نظر'].apply(preprocess_comment)
df['تگ‌ها پاکسازی‌شده'] = df['تگ های کامنت'].apply(clean_tags)
df['نام پاکسازی‌شده'] = df['نام پزشک'].apply(clean_name)
df['تخصص پاکسازی‌شده'] = df['تخصص'].apply(clean_specialty)


os.makedirs("output", exist_ok=True)
df.to_excel(OUTPUT_FILE, index=False)
print("✅ پیش‌پردازش با موفقیت انجام شد. فایل خروجی در مسیر 'output/' ذخیره شد.")

