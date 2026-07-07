import pandas as pd
import re

def run_quality_checks(df):

    results = {}

    # Missing Values
    results["missing_values"] = df.isnull().sum().sum()

    # Duplicate Rows
    results["duplicates"] = df.duplicated().sum()

    # Invalid Age
    if "age" in df.columns:
        results["invalid_age"] = df[df["age"] < 0]

    # Invalid Email
    if "email" in df.columns:
        results["invalid_email"] = df[
            abs(df["email"].fillna("").str.count("@") - 1) > 0
        ]

    # Invalid Phone
    if "phone" in df.columns:

        def is_invalid_phone(phone):

            phone = re.sub(r"\D", "", str(phone))

            if phone.startswith("94"):
                phone = "0" + phone[2:]

            return len(phone) != 10

        results["invalid_phone"] = df[
            df["phone"].apply(is_invalid_phone)
        ]

    # Invalid Join Date
    if "join_date" in df.columns:
        results["invalid_join_date"] = df[
            pd.to_datetime(df["join_date"], errors="coerce").isnull()
        ]

    return results