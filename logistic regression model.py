import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer


df = pd.read_excel("data/filtered_balanced_tags.xlsx")


tag_columns = [
    'توضیحات و مشاوره دقیق', 'زمان انتظار کم',
    'محیط تمیز و آرام', 'نوبتدهی آنلاین'
]


X_text = df['نظر '].fillna("")
y = df[tag_columns]


vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(X_text)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = MultiOutputClassifier(LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("📊 گزارش عملکرد مدل:\n")
print(classification_report(y_test, y_pred, target_names=tag_columns))


all_predictions = model.predict(X)
predicted_df = pd.DataFrame(all_predictions, columns=[f"پیش‌بینی_{col}" for col in tag_columns])


output_df = pd.concat([df.reset_index(drop=True), predicted_df], axis=1)
output_df.to_excel("data/نتایج_پیش‌بینی_تگ‌ها.xlsx", index=False)


print("✅ فایل خروجی با پیش‌بینی تگ‌ها ذخیره شد در: data/نتایج_پیش‌بینی_تگ‌ها.xlsx")
