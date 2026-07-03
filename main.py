from src.load_data import load_data
from src.quality_checks import check_missing_values, check_duplicates, check_invalid_age, check_invalid_email, check_invalid_phone  
from src.report_generator import generate_report

df = load_data("data/raw/customer.csv")
print(df.head())
print(df.shape)
print(df.columns)
df.info()
print(df.describe())

print("Missing Values:\n", check_missing_values(df))
print("Duplicate Rows:\n", check_duplicates(df))
print("invalid Age Entities :\n",check_invalid_age(df))
print("invalid Email Entities :\n",check_invalid_email(df))
print("invalid Phone Entities :\n",check_invalid_phone(df))


print("\nGenerating Data Quality Report...")
missing_values = check_missing_values(df).sum()
duplicates = check_duplicates(df)
invalid_age = check_invalid_age(df)
invalid_email = check_invalid_email(df)
invalid_phone = check_invalid_phone(df)

generate_report(df, missing_values, duplicates, invalid_age, invalid_email, invalid_phone)