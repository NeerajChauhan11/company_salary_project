import pandas as pd
import numpy as np
from db_engine import get_engine
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# ------------------------
# Load Data
# ------------------------

engine = get_engine()
df = pd.read_sql("SELECT * FROM company_salary_data", engine)

# ------------------------
# Outlier Handling (same as preprocessing)
# ------------------------

Q1 = df["ctc"].quantile(0.25)
Q3 = df["ctc"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df["ctc"] = np.where(df["ctc"] > upper, upper, df["ctc"])
df["ctc"] = np.where(df["ctc"] < lower, lower, df["ctc"])

# ------------------------
# Feature / Target split
# ------------------------

X = df.drop(columns=["id", "employee_name", "ctc"])
y = df["ctc"]

categorical_cols = ["company_name", "department", "role", "location"]
numerical_cols = ["experience_years", "performance_rating"]

# ------------------------
# Encoding
# ------------------------

encoder = OneHotEncoder(sparse_output=False, drop="first")
encoded = encoder.fit_transform(X[categorical_cols])

encoded_df = pd.DataFrame(
    encoded, columns=encoder.get_feature_names_out(categorical_cols)
)

# ------------------------
# Scaling
# ------------------------

scaler = StandardScaler()
scaled = scaler.fit_transform(X[numerical_cols])

scaled_df = pd.DataFrame(scaled, columns=numerical_cols)

# ------------------------
# Final Dataset
# ------------------------

final_X = pd.concat([scaled_df, encoded_df], axis=1)

# ------------------------
# Train-Test Split
# ------------------------

X_train, X_test, y_train, y_test = train_test_split(
    final_X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# ------------------------
# Model 1: Linear Regression
# ------------------------

lr = LinearRegression()
lr.fit(X_train, y_train)

lr_preds = lr.predict(X_test)

lr_r2 = r2_score(y_test, lr_preds)
lr_mae = mean_absolute_error(y_test, lr_preds)

print("\n📈 Linear Regression Performance")
print("R2 Score:", round(lr_r2, 3))
print("MAE:", round(lr_mae, 2))

# ------------------------
# Model 2: Random Forest
# ------------------------

rf = RandomForestRegressor(n_estimators=200, random_state=42)

rf.fit(X_train, y_train)

rf_preds = rf.predict(X_test)

rf_r2 = r2_score(y_test, rf_preds)
rf_mae = mean_absolute_error(y_test, rf_preds)

print("\n🌳 Random Forest Performance")
print("R2 Score:", round(rf_r2, 3))
print("MAE:", round(rf_mae, 2))

# ------------------------
# Simple Prediction Example
# ------------------------

sample_input = X_test.iloc[0:1]

predicted_salary = rf.predict(sample_input)[0]

print("\n💰 Sample Predicted Salary (LPA):", round(predicted_salary, 2))
print("Actual Salary:", round(y_test.iloc[0], 2))
