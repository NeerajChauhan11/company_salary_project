import pandas as pd
import numpy as np
from db_engine import get_engine
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)

X = df.drop(columns=["id", "employee_name", "ctc"])
y = df["ctc"]

cat_cols = ["company_name", "department", "role", "location"]
num_cols = ["experience_years", "performance_rating"]

encoder = OneHotEncoder(drop="first", sparse_output=False)
X_cat = encoder.fit_transform(X[cat_cols])

scaler = StandardScaler()
X_num = scaler.fit_transform(X[num_cols])

final_X = np.hstack([X_num, X_cat])

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(final_X, y)

def predict_salary(company, department, role, location, experience, rating):

    user_df = pd.DataFrame([{
        "company_name": company,
        "department": department,
        "role": role,
        "location": location,
        "experience_years": experience,
        "performance_rating": rating
    }])

    user_cat = encoder.transform(user_df[cat_cols])
    user_num = scaler.transform(user_df[num_cols])

    user_final = np.hstack([user_num, user_cat])

    salary = model.predict(user_final)[0]

    return round(salary,2)

# Example
print("\nPredicted Salary:",
      predict_salary("Google","IT","AI Engineer","Bangalore",6,5),
      "LPA")
