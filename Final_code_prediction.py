import pandas as pd

# -------------------- 1. بارگذاری داده‌ها (فایل خروجی با پیش‌بینی‌ها) --------------------
df = pd.read_excel("data/نتایج_پیش‌بینی_تگ‌ها.xlsx")  # ← فایل خروجی مدل قبلی

# فرض می‌کنیم ستون‌های پیش‌بینی با پیشوند "پیش‌بینی_" هستند
tag_columns = ['توضیحات و مشاوره دقیق', 'زمان انتظار کم', 'محیط تمیز و آرام', 'نوبتدهی آنلاین']
pred_columns = [f"پیش‌بینی_{tag}" for tag in tag_columns]

# -------------------- 2. محاسبه میانگین تگ‌ها برای هر دکتر بر اساس پیش‌بینی‌ها --------------------
doctor_scores = df.groupby("نام")[pred_columns].mean().reset_index()

# الحاق تخصص دکتر (فرض: هر دکتر یک تخصص دارد)
doctor_specialty = df.groupby("نام")["تخصص "].first().reset_index()
doctor_scores = doctor_scores.merge(doctor_specialty, on="نام")

# -------------------- 3. انتخاب بهترین دکتر هر تخصص --------------------
best_doctors = (
    doctor_scores
    .sort_values(by=pred_columns, ascending=False)
    .groupby("تخصص ")
    .head(1)
    .reset_index(drop=True)
)

# -------------------- 4. نمایش خروجی --------------------
print("\n🏆 بهترین دکترها بر اساس تحلیل پیش‌بینی مدل:")
for _, row in best_doctors.iterrows():
    print(f"تخصص: {row['تخصص ']} → 👨‍⚕️ {row['نام']}")
    for col in pred_columns:
        tag = col.replace("پیش‌بینی_", "")
        print(f"   🏷️ {tag}: {row[col]:.2f}")
    print()