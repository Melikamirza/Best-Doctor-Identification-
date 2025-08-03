from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
# راه‌اندازی درایور
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# لینک لیست دکترها
url = "https://doctor-yab.ir/Search/City-7/Takhasos-1045/?page=2"
driver.get(url)

span_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "HaveAreception")))
doctor_links = []

for btn in span_buttons:
    try:
        parent_a = btn.find_element(By.XPATH, "./ancestor::a")
        href = parent_a.get_attribute("href")
        if href:
            doctor_links.append(href)
    except:
        continue

new_data = []

# پیمایش لینک‌ها
for i, link in enumerate(doctor_links):
    try:
        driver.get(link)
        time.sleep(2)

        # گرفتن نام و تخصص
        try:
            name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fgth1name"))).text.strip()
            specialty = driver.find_element(By.CLASS_NAME, "a-description").text.strip()
        except:
            continue  
        # گرفتن کامنت‌ها
        doctor_comments = driver.find_elements(By.CLASS_NAME, "comment-text")
        has_valid_comment = False

        for comment_block in doctor_comments:
            try:
                all_p_tags = comment_block.find_elements(By.TAG_NAME, "p")
                clean_text = all_p_tags[2].text.strip() if len(all_p_tags) >= 3 else ""

                if not clean_text:
                    continue  

                tags_list = comment_block.find_elements(By.XPATH, ".//ul/li[@class='like']")
                tags = ", ".join([tag.text.strip() for tag in tags_list if tag.text.strip()]) or "بدون تگ"

                # ذخیره اطلاعات
                new_data.append({
                    "نام پزشک": name,
                    "تخصص": specialty,
                    "نظر": clean_text,
                    "تگ‌های کامنت": tags
                })

                has_valid_comment = True

            except:
                continue

        if not has_valid_comment:
            print(f"⏭️ دکتر {name} بدون کامنت معتبر رد شد.")

    except Exception as e:
        print(f"❌ خطا در دکتر {i+1}: {e}")

# ذخیره در اکسل
file_path = "C:/Users/Quantom/Desktop/uni/doctor_info.xlsx"
df_new = pd.DataFrame(new_data)

if os.path.exists(file_path):
    df_existing = pd.read_excel(file_path, engine="openpyxl")
    final_df = pd.concat([df_existing, df_new], ignore_index=True)
else:
    final_df = df_new

final_df.drop_duplicates(inplace=True)
final_df.to_excel(file_path, index=False, engine="openpyxl")
print("\n✅ فقط دکترهای دارای کامنت ذخیره شدند.")
driver.quit()
