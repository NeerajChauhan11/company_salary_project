import pandas as pd
from db_engine import get_engine

engine = get_engine()

df = pd.read_sql("SELECT * FROM company_salary_data", engine)

print("\nFirst 5 rows:")
print(df.head())

print("\nShape of data (rows, columns):")
print(df.shape)

print("\nColumn info:")
print(df.info())

