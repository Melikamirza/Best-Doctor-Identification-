import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------------------
# 1. بارگذاری داده متوازن‌شده
# -------------------------------
df = pd.read_excel("data/filtered_balanced_tags.xlsx")

# -------------------------------
# 2. تعریف ستون‌ها
# -------------------------------
tag_columns = [
    'توضیحات و مشاوره دقیق', 'زمان انتظار کم',
    'محیط تمیز و آرام', 'نوبتدهی آنلاین'
]

# -------------------------------
# 3. پیش‌پردازش متن
# -------------------------------
X_text = df['نظر '].fillna("")   # حذف NaNها
y = df[tag_columns]

# -------------------------------
# 4. بردارسازی متن با TF-IDF
# -------------------------------
vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(X_text)

# -------------------------------
# 5. تقسیم داده به train/test
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 6. آموزش مدل
# -------------------------------
model = MultiOutputClassifier(LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)

# -------------------------------
# 7. ارزیابی مدل
# -------------------------------
y_pred = model.predict(X_test)
print("📊 گزارش عملکرد مدل:\n")
print(classification_report(y_test, y_pred, target_names=tag_columns))

# -------------------------------
# 8. پیش‌بینی تگ‌ها برای کل داده‌ها
# -------------------------------
all_predictions = model.predict(X)
predicted_df = pd.DataFrame(all_predictions, columns=[f"پیش‌بینی_{col}" for col in tag_columns])

# -------------------------------
# 9. ترکیب با داده اصلی و ذخیره خروجی
# -------------------------------
output_df = pd.concat([df.reset_index(drop=True), predicted_df], axis=1)
output_df.to_excel("data/نتایج_پیش‌بینی_تگ‌ها.xlsx", index=False)

print("✅ فایل خروجی با پیش‌بینی تگ‌ها ذخیره شد در: data/نتایج_پیش‌بینی_تگ‌ها.xlsx")