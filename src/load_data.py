import pandas as pd

def load_data(file):
    return pd.read_csv(file, dtype={"phone": str})