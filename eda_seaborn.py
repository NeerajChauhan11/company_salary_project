import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_engine import get_engine

# loading the data
engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)
sns.set(style="whitegrid")

print("\nDataset shape:", df.shape)

# Salary distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["ctc"], kde=True)
plt.title("Salary Distributions (CTC)")
plt.show()


plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="experience_years", y="ctc")
sns.regplot(data=df, x="experience_years", y="ctc", scatter=False)
plt.title("Experience vs Salary Trend")
plt.show()

# ---------------------------
# 3️⃣ Company wise salary (boxplot)
# ---------------------------

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="company_name", y="ctc")
plt.title("Company Wise Salary Distribution")
plt.xticks(rotation=45)
plt.show()

# ---------------------------
# 4️⃣ Performance vs Salary
# ---------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="performance_rating", y="ctc")
plt.title("Performance Rating vs Salary")
plt.show()
