import os 
import pandas as pd

def standardize_files(directory):
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            df = pd.read_csv(file)
            # Standardize column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            # Standardize dates
            date_columns = [col for col in df.columns if 'date' in col]
            for date_col in date_columns:
                df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')
            # Save standardized file
            df.to_csv(f'standardized_{file}', index=False)