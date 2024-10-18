#pip install polars
import polars as pl
file_path = 'D:/GambillDataEngineering/Data sets/'
# Load a CSV file
df = pl.read_csv(f'{file_path}pandas_tutorial.csv')
print(df.head())  # Display the first few rows

# Load a Parquet file
parquet_df = pl.read_parquet(f'{file_path}large_data.parquet')
#print(parquet_df.head())
#print(df.filter(pl.col("age").is_null()))
#df = df.fill_null(0)  # Replace missing values with 0
#df = df.drop_nulls(['age'])  # Drop rows missing 'important_column'
#print(df.head(20))

result = parquet_df.with_columns((parquet_df['salary'] * 2).alias('new_salary'))
print(result.head())