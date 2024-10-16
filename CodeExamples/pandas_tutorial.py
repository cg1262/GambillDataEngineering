#pip install pandas
import pandas as pd
file_path = 'D:/GambillDataEngineering/Data sets/'
file_name = f'{file_path}pandas_tutorial'

processed_chunks = []

for chunk in pd.read_csv(f'{file_path}large_data.csv', chunksize=10000):
    chunk['Salary_W_Merit_Increase'] = chunk['salary'] * 1.05
    print(chunk.head())  # Example of processing each chunk
    processed_chunks.append(chunk)

final_df = pd.concat(processed_chunks)
print(final_df.head())
"""
print("**********************\nCSV Dataframe fillna:")
csv_data.fillna(0,inplace=True) # Replace missing values with 0
print(csv_data)

csv_data = pd.read_csv(f'{file_name}.csv')
print("**********************\ncsv_original replaced in csv_data Dataframe:")
print(csv_data.head())

print("**********************\nCSV Dataframe dropna:")
csv_data.dropna(subset=['age'], inplace=True) # Drop rows missing 'age'
print(csv_data)

csv_data = pd.read_csv(f'{file_name}.csv')
print("**********************\ncsv_original replaced in csv_data Dataframe:")
print(csv_data)

print("**********************\nCSV Dataframe drop duplicates:")
csv_data.drop_duplicates(subset='id', inplace=True) # Drop rows missing 'age'
print(csv_data)

processed_chunks = []

for chunk in pd.read_csv(f'{file_path}large_data.csv', chunksize=10000):
    chunk['Salary_W_Merit_Increase'] = chunk['salary'] * 1.05
    print(chunk.head())  # Example of processing each chunk
    processed_chunks.append(chunk)

final_df = pd.concat(processed_chunks)
print(final_df.head())

import pandas as pd
file_path = 'D:/GambillDataEngineering/Data sets/'
file_name = f'{file_path}pandas_tutorial'
csv_data = pd.read_csv(f'{file_name}.csv')
print("**********************\nCSV Dataframe:")
print(csv_data.head())  # Shows first 5 rows of the dataset
json_data = pd.read_json(f'{file_name}.json')
print("**********************\nJSON Dataframe:")
print(json_data.head())

parquet_data = pd.read_parquet(f"{file_name}.parquet")
print("**********************\nParquet Dataframe:")
print(parquet_data.head())

"""