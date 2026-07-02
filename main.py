from src.load_data import load_data

df = load_data("data/raw/customer.csv")
print(df.head())