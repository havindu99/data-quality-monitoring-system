def generate_report(df, missing_values, duplicates, invalid_age, invalid_email, invalid_phone):

    print("\n" + "=" * 50)
    print("        DATA QUALITY REPORT")
    print("=" * 50)

    print(f"Total Records: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")

    print(f"Missing Values: {missing_values}")
    print(f"Duplicate Rows: {duplicates}")

    print(f"Invalid Age Entities: {len(invalid_age)}")
    print(f"Invalid Email Entities: {len(invalid_email)}")
    print(f"Invalid Phone Entities: {len(invalid_phone)}")

    print("=" * 50)