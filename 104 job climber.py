from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import csv
import os
#pip install selenium webdriver-manager

# 初始化 Edge 瀏覽器（無頭模式）
options = Options()
options.use_chromium = True
options.add_argument("--headless")  # 如要顯示瀏覽器，註解這行
options.add_argument("--disable-gpu")

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)


# 開啟 104 搜尋頁面
driver.get("https://www.104.com.tw/jobs/search/?jobcat=2007000000&jobsource=index_s&mode=s")
time.sleep(3)

# 等待第一筆職缺內容載入
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "h2 > a.info-job"))
)

# 儲存已擷取的職缺（避免重複）
seen_titles = set()
job_data = []



# 模擬向下滾動以觸發 Vue 懶加載
for scroll in range(10):  # 可調整滾動次數（每次大約 10-15 筆）
    driver.execute_script("window.scrollBy(0, 3600);")
    time.sleep(1.5)

    cards = driver.find_elements(By.CSS_SELECTOR, "div.vue-recycle-scroller__item-view")
    print(f"第 {scroll+1} 次滾動：偵測到 {len(cards)} 筆元素")

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2 > a.info-job").text.strip()
            if title in seen_titles or title == "":
                continue
            seen_titles.add(title)

            company = card.find_element(By.CSS_SELECTOR, "div.info-company a").text.strip()
            region = card.find_element(By.CSS_SELECTOR, "div.info-tags a[data-gtm-joblist*='地區']").text.strip()
            experience = card.find_element(By.CSS_SELECTOR, "div.info-tags a[data-gtm-joblist*='經歷']").text.strip()
            education = card.find_element(By.CSS_SELECTOR, "div.info-tags a[data-gtm-joblist*='學歷']").text.strip()
            salary = card.find_element(By.CSS_SELECTOR, "div.info-tags a[data-gtm-joblist*='薪資']").text.strip()

            job_data.append([title, company, region, experience, education, salary])
        except Exception as e:
            # 若某些欄位沒載入成功就跳過
            continue

# 關閉瀏覽器
driver.quit()

# 匯出 CSV
folder_path = "C:\\Users\\User\\Downloads\\104-web-climber-main"
os.makedirs(folder_path, exist_ok=True)  # 若資料夾不存在就建立

# 建立完整檔案路徑
csv_path = os.path.join(folder_path, "104_jobs.csv")

# 寫入 CSV
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["職缺名稱", "公司名稱", "工作地區", "經歷需求", "學歷需求", "薪資待遇"])
    print("準備寫入 CSV，共", len(job_data), "筆資料")
    writer.writerows(job_data)

print("✅ CSV 已儲存到：", csv_path)

print("✅ 完成！已輸出到 104_jobs.csv，共", len(job_data), "筆資料。")
