import pandas as pd
import random
import datetime

# Set random seed for reproducibility
random.seed(42)

# Define ranges and sample data for generating the dataset
regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Furniture', 'Books', 'Toys']
num_records = 1000000  # 1 million records
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='H').to_pydatetime().tolist()

# Generate the dataset
data = {
    'OrderDate': random.choices(date_range, k=num_records),
    'Region': random.choices(regions, k=num_records),
    'ProductCategory': random.choices(categories, k=num_records),
    'SalesAmount': [round(random.uniform(5, 500), 2) for _ in range(num_records)],
    'Quantity': [random.randint(1, 100) for _ in range(num_records)]
}

# Create DataFrame
df_sales = pd.DataFrame(data)

# Save to CSV file
csv_file_path = 'D:/data/sales_data_october_challenge.csv'
df_sales.to_csv(csv_file_path, index=False)

csv_file_path
