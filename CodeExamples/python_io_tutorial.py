import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Name': ['Chris', 'Anna', 'John'],
    'Age': [30, 29, 32],
    'Occupation': ['Data Engineer', 'Analyst', 'Manager']
})

# Writing to a Parquet file
df.to_parquet('people.parquet')

# Reading from a Parquet file
df_parquet = pd.read_parquet('people.parquet')
print(df_parquet)
