import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 設定中文字型（Windows）
plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

# 讀取資料
file_path = r"C:\\Users\\User\Downloads\\104_jobs.csv"  # 請根據你的實際路徑修改
df = pd.read_csv(file_path)

# 顯示欄位確認
print("欄位名稱：", df.columns.tolist())

# 指定正確欄位名稱（根據你的圖片）
columns_needed = ['薪資待遇', '學歷需求', '經歷需求']
df = df[columns_needed].dropna()

# 轉換薪資為月薪
def salary_to_month(salary_str):
    if not isinstance(salary_str, str):
        return None

    # 擷取數字
    nums = re.findall(r'(\d[\d,]*)', salary_str)
    nums = [int(n.replace(',', '')) for n in nums]
    if not nums:
        return None
    avg = sum(nums) / len(nums)

    if '時薪' in salary_str:
        return round(avg * 8 * 22)
    elif '日薪' in salary_str:
        return round(avg * 22)
    elif '週薪' in salary_str:
        return round(avg * 4.33)
    elif '年薪' in salary_str:
        return round(avg / 12)
    elif '月薪' in salary_str:
        return round(avg)
    else:
        return None

# 應用轉換函數
df['月薪'] = df['薪資待遇'].apply(salary_to_month)

# 移除無效月薪
df = df.dropna(subset=['月薪'])

# 顯示前幾筆資料確認
print(df[['薪資待遇', '月薪', '學歷需求', '經歷需求']].head())

# 分析學歷與經歷對月薪的影響
edu_salary = df.groupby('學歷需求')['月薪'].mean().sort_values(ascending=False)
exp_salary = df.groupby('經歷需求')['月薪'].mean().sort_values(ascending=False)

# 繪製圖表
plt.figure(figsize=(16, 6))

# 學歷圖
plt.subplot(1, 2, 1)
sns.barplot(x=edu_salary.values, y=edu_salary.index, palette='Blues_r')
plt.title('不同學歷的平均月薪')
plt.xlabel('平均月薪（元）')
plt.ylabel('學歷')

# 經歷圖
plt.subplot(1, 2, 2)
sns.barplot(x=exp_salary.values, y=exp_salary.index, palette='Greens_r')
plt.title('不同工作經歷的平均月薪')
plt.xlabel('平均月薪（元）')
plt.ylabel('經歷')

plt.tight_layout()
plt.show()
