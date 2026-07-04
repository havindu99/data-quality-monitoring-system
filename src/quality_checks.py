import pandas as pd



def run_quality_checks(df):
    results = {}

    results["missing_values"] = df.isnull().sum().sum()
    results["duplicates"] = df.duplicated().sum()

    if "age" in df.columns:
        results["invalid_age"] = df[df["age"] < 0]

    if "email" in df.columns:
        results["invalid_email"] = df[abs(df["email"].astype(str).str.count("@") - 1) > 0]

    if "phone" in df.columns:
        results["invalid_phone"] = df[df["phone"].astype(str).str.len() != 10]

    if "join_date" in df.columns:
        results["invalid_join_date"] = df[
            pd.to_datetime(df["join_date"], errors="coerce").isnull()
        ]

    return results