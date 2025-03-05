import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# Generating a dataset with about 1 million records for the SQL Optimization Challenge
# Dataset fields: 'TransactionID', 'CustomerID', 'ProductID', 'TransactionDate', 'Quantity', 'UnitPrice'

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

# Generate data
num_records = 1000000

# Transaction IDs (unique)
transaction_ids = range(1, num_records + 1)

# Customer IDs (randomly generated in the range of 1 to 10000)
customer_ids = [random.randint(1, 10000) for _ in range(num_records)]

# Product IDs (randomly generated in the range of 1 to 100)
product_ids = [random.randint(1, 100) for _ in range(num_records)]

# Transaction Dates (random dates within the last 2 years)
start_date = datetime.now() - timedelta(days=2 * 365)
transaction_dates = [start_date + timedelta(days=random.randint(0, 730)) for _ in range(num_records)]

# Quantities (randomly generated in the range of 1 to 20)
quantities = [random.randint(1, 20) for _ in range(num_records)]

# Unit Prices (randomly generated between 5.00 and 100.00)
unit_prices = [round(random.uniform(5, 100), 2) for _ in range(num_records)]

# Create DataFrame
data = {
    'TransactionID': transaction_ids,
    'CustomerID': customer_ids,
    'ProductID': product_ids,
    'TransactionDate': transaction_dates,
    'Quantity': quantities,
    'UnitPrice': unit_prices
}

df = pd.DataFrame(data)

# Saving the dataset as a CSV file
file_path = "D:/data/large_sales_transactions.csv"
df.to_csv(file_path, index=False)

file_path
