import pandas as pd

def load_data(file_path=r'C:\Users\hyusuf011\OneDrive - PwC\Professional Final Project Data Analysis\Data\data.csv'):
    data = pd.read_csv(file_path) 
    return data
