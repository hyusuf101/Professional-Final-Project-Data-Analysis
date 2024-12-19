import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    data.to_csv('data/raw/data.csv', index=False)  # Save raw data
    return data
