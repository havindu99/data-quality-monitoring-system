import pandas as pd
import numpy as np


def profile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a per-column summary table:
    dtype, missing %, unique count, and (for numeric columns)
    min / max / mean / std / outlier count via the IQR method.
    """
    rows = []
    for col in df.columns:
        series = df[col]
        row = {
            "Column": col,
            "Type": str(series.dtype),
            "Missing %": round(series.isnull().mean() * 100, 1),
            "Unique Values": series.nunique(dropna=True),
        }

        if pd.api.types.is_numeric_dtype(series):
            clean = series.dropna()
            if len(clean) > 0:
                q1 = clean.quantile(0.25)
                q3 = clean.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = clean[(clean < lower) | (clean > upper)]

                row["Min"] = round(clean.min(), 2)
                row["Max"] = round(clean.max(), 2)
                row["Mean"] = round(clean.mean(), 2)
                row["Std Dev"] = round(clean.std(), 2)
                row["Outliers"] = len(outliers)
            else:
                row["Min"] = row["Max"] = row["Mean"] = row["Std Dev"] = row["Outliers"] = None
        else:
            row["Min"] = row["Max"] = row["Mean"] = row["Std Dev"] = row["Outliers"] = "-"

        rows.append(row)

    return pd.DataFrame(rows)


def get_outlier_rows(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Returns the full rows of df that are outliers for a given numeric column."""
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return pd.DataFrame()

    clean = df[column].dropna()
    if len(clean) == 0:
        return pd.DataFrame()

    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[(df[column] < lower) | (df[column] > upper)]