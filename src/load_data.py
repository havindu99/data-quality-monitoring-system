import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path, dtype={"phone": str})
    return df