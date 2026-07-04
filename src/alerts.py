import pandas as pd

def check_alerts(df):
    alerts = {}
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        alerts['missing_values'] = missing_values[missing_values > 0].to_dict()
    
    # Check for duplicate rows
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        alerts['duplicate_rows'] = duplicate_rows
    
    # Check for invalid age (negative values)
    invalid_age = df[df["age"] < 0]
    if not invalid_age.empty:
        alerts['invalid_age'] = invalid_age.to_dict(orient='records')
    
    # Check for invalid email (not containing '@')
    invalid_email = df[abs(df["email"].astype(str).str.count("@") - 1) > 0]
    if not invalid_email.empty:
        alerts['invalid_email'] = invalid_email.to_dict(orient='records')
    
    # Check for invalid phone (not 10 digits)
    invalid_phone = df[abs(df["phone"].astype(str).str.len() - 10) > 0]
    if not invalid_phone.empty:
        alerts['invalid_phone'] = invalid_phone.to_dict(orient='records')

    # Check for invalid join_date (not a valid date)
    invalid_join_date = df[pd.to_datetime(df["join_date"], errors='coerce').isnull()]
    if not invalid_join_date.empty:
        alerts['invalid_join_date'] = invalid_join_date.to_dict(orient='records')
        
    
    return alerts