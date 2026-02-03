import pandas as pd
from db_engine import get_engine

engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)

print("\n=========SALARY ANALYTICS REPORT===========")

company_avg = df.groupby("company_name")["ctc"].mean().sort_values(ascending=False)

print("🏢 Company wise average Sarlar:\n")
print(company_avg)

# 2️⃣ Experience vs salary trend
exp_salary = df.groupby("experience_years")["ctc"].mean()

print("\n📈 Experience vs Average Salary:\n")
print(exp_salary)

# 3️⃣ Performance impact
performance_salary = df.groupby("performance_rating")["ctc"].mean()

print("\n⭐ Performance Rating vs Salary:\n")
print(performance_salary)

# 4️⃣ Top paying employees
top_paid = df.sort_values("ctc", ascending=False).head(10)

print("\n💰 Top 10 Highest Paid Employees:\n")
print(top_paid[["employee_name", "company_name", "ctc"]])
