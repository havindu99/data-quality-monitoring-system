import os
import pandas as pd
from datetime import datetime

HISTORY_COLUMNS = ["timestamp", "file_name", "records", "columns", "issues", "score"]


def save_run(history_path: str, file_name: str, records: int, columns: int,
             issues: int, score: float):
    """Appends one run's summary to the history CSV, creating it if needed."""
    os.makedirs(os.path.dirname(history_path), exist_ok=True)

    new_row = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_name": file_name,
        "records": records,
        "columns": columns,
        "issues": issues,
        "score": score,
    }])

    if os.path.exists(history_path):
        history_df = pd.read_csv(history_path)
        history_df = pd.concat([history_df, new_row], ignore_index=True)
    else:
        history_df = new_row

    history_df.to_csv(history_path, index=False)


def load_history(history_path: str) -> pd.DataFrame:
    """Loads the run history, or an empty frame with the right columns if none exists yet."""
    if os.path.exists(history_path):
        return pd.read_csv(history_path)
    return pd.DataFrame(columns=HISTORY_COLUMNS)