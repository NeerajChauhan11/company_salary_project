import pandas as pd
import numpy as np
from db_engine import get_engine
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)

# Outlier capping
Q1 = df["ctc"].quantile(0.25)
Q3 = df["ctc"].quantile(0.75)
IQR = Q3 - Q1

df["ctc"] = np.clip(df["ctc"], Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

X = df.drop(columns=["id", "employee_name", "ctc"])
y = df["ctc"]

cat_cols = ["company_name", "department", "role", "location"]
num_cols = ["experience_years", "performance_rating"]

encoder = OneHotEncoder(drop="first", sparse_output=False)
encoded = encoder.fit_transform(X[cat_cols])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))

scaler = StandardScaler()
scaled = scaler.fit_transform(X[num_cols])
scaled_df = pd.DataFrame(scaled, columns=num_cols)

final_X = pd.concat([scaled_df, encoded_df], axis=1)

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(final_X, y)

importance = pd.Series(rf.feature_importances_, index=final_X.columns)
importance = importance.sort_values(ascending=False)

print("\n🔥 FEATURE IMPORTANCE (Top factors affecting salary):\n")
print(importance.head(15))
