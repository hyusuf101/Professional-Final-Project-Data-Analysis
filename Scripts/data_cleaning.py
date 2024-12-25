import pandas as pd

def clean_data(df):
    # Rename the first two columns
    df.rename(columns={df.columns[0]: 'Crime Category', df.columns[1]: 'Subcategory'}, inplace=True)
    
    # Format the rest of the columns to be dates
    for col in df.columns[3:]:
        try:
            # Try converting the column name to a datetime format to see if it's a valid date
            formatted_date = pd.to_datetime(col, format='%Y%m').strftime('%Y-%m')
            df.rename(columns={col: formatted_date}, inplace=True)
        except ValueError:
            # If the conversion fails, print a message and skip renaming
            print(f"Column {col} is not in the expected date format and will not be renamed.")

    if 'BoroughName' in df.columns:
        df.rename(columns={'BoroughName': 'Borough'}, inplace=True)

    # Drop rows with missing values
    df = df.dropna()  
    
    return df

