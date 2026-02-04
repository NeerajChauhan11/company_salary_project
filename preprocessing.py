import pandas as pd
import numpy as np
from db_engine import get_engine
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Loading the Data
engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)

print("Original Shape:", df.shape)

# Outlier Handling
Q1 = df["ctc"].quantile(0.25)
Q3 = df["ctc"].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 - 1.5 * IQR

df["ctc"] = np.where(df["ctc"] > upper_limit, upper_limit, df["ctc"])
df["ctc"] = np.where(df["ctc"] < lower_limit, lower_limit, df["ctc"])

print("Outliers capped")

# ------------------------
# 2️⃣ Separate features & target
# ------------------------

X = df.drop(columns=["id", "employee_name", "ctc"])
y = df["ctc"]

# ------------------------
# 3️⃣ One-Hot Encode Categorical columns
# ------------------------

categorical_cols = ["company_name", "department", "role", "location"]

encoder = OneHotEncoder(sparse=False, drop="first")
encoded_data = encoder.fit_transform(X[categorical_cols])

encoded_df = pd.DataFrame(
    encoded_data,
    columns = encoder.get_feature_names_out(categorical_cols)
)


#Now scaling the numerical features

numerical_cols = ["experience_years", "performance_rating"]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(X[numerical_cols])

scaled_df = pd.DataFrame(
    scaled_data,
    columns=numerical_cols
)

#combine final dataset

final_X  = pd.concat([scaled_df, encoded_df], axis=1)
print("\n Final feature matrix shape:", final_X.shape)
print("\nSample cleaned dataset:")
print(final_X.head())

print("\nPreprocessing completed sucessfully!")
