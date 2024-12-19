import pandas as pd

def clean_data(df):
    # Rename the first two columns
    df.rename(columns={df.columns[0]: 'Crime Category', df.columns[1]: 'Subcategory'}, inplace=True)
    
    # Format the rest of the columns to be dates
    for col in df.columns[3:]:
        df.rename(columns={col: pd.to_datetime(col, format='%Y%m').strftime('%Y-%m')}, inplace=True)
    
  
    df = df.dropna()  # Drop rows with missing values
    
    return df
