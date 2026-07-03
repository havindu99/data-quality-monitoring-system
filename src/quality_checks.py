import pandas as pd

def check_missing_values(df):
    return df.isnull().sum()
def check_duplicates(df):
    return df.duplicated().sum()
def check_invalid_age(df):
    return df[df["age"] < 0]
def check_invalid_email(df):
    return df[abs(df["email"].astype(str).str.count("@") - 1) > 0]
def check_invalid_phone(df):
    return df[abs(df["phone"].astype(str).str.len() - 10) > 0]