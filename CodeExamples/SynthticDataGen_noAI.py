import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import sqlalchemy

fake = Faker()
Faker.seed(0)
np.random.seed(0)

# Parameters
num_customers = 500000  # Half a million customers
num_orders = 2000000    # Two million orders
num_order_items = 5000000  # Assume each order has 2-3 items on average

# Generate Customers Data
def generate_customers(num_customers):
    customer_ids = range(1, num_customers + 1)
    data = {
        'customer_id': customer_ids,
        'customer_name': [fake.name() for _ in customer_ids],
        'customer_email': [fake.email() for _ in customer_ids],
        'customer_phone': [fake.phone_number() for _ in customer_ids],
        'customer_address': [fake.street_address() for _ in customer_ids],
        'customer_city': [fake.city() for _ in customer_ids],
        'customer_state': [fake.state() for _ in customer_ids],
        'customer_zip': [fake.zipcode() for _ in customer_ids],
        'customer_country': [fake.country() for _ in customer_ids],
        'registration_date': [fake.date_between(start_date='-5y', end_date='today') for _ in customer_ids]
    }
    customers_df = pd.DataFrame(data)
    return customers_df

# Generate Orders Data
def generate_orders(num_orders, num_customers):
    order_ids = range(1, num_orders + 1)
    data = {
        'order_id': order_ids,
        'customer_id': np.random.randint(1, num_customers + 1, num_orders),
        'order_date': [fake.date_between(start_date='-1y', end_date='today') for _ in order_ids],
        'order_total': np.round(np.random.uniform(10.0, 500.0, num_orders), 2),
        'order_status': np.random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'], num_orders),
        'shipping_address': [fake.street_address() for _ in order_ids],
        'shipping_city': [fake.city() for _ in order_ids],
        'shipping_state': [fake.state() for _ in order_ids],
        'shipping_zip': [fake.zipcode() for _ in order_ids],
        'shipping_country': [fake.country() for _ in order_ids],
    }
    orders_df = pd.DataFrame(data)
    return orders_df

# Generate Order Items Data
def generate_order_items(num_order_items, num_orders):
    order_item_ids = range(1, num_order_items + 1)
    data = {
        'order_item_id': order_item_ids,
        'order_id': np.random.randint(1, num_orders + 1, num_order_items),
        'product_id': np.random.randint(1, 1000, num_order_items),
        'product_name': np.random.choice(['Coca-Cola Classic', 'Coca-Cola Zero Sugar', 'Diet Coke', 'Sprite', 'Fanta', 'Dasani Water', 'Minute Maid Juice'], num_order_items),
        'product_category': np.random.choice(['Soda', 'Water', 'Juice'], num_order_items),
        'quantity': np.random.randint(1, 10, num_order_items),
        'unit_price': np.round(np.random.uniform(1.0, 5.0, num_order_items), 2),
    }
    df = pd.DataFrame(data)
    df['total_price'] = np.round(df['quantity'] * df['unit_price'], 2)
    return df

# Generate DataFrames
print("Generating customers data...")
customers_df = generate_customers(num_customers)

print("Generating orders data...")
orders_df = generate_orders(num_orders, num_customers)

print("Generating order items data...")
order_items_df = generate_order_items(num_order_items, num_orders)

# Save DataFrames to Parquet files
print("Saving data to Parquet files...")
customers_df.to_parquet('customers.parquet', index=False)
orders_df.to_parquet('orders.parquet', index=False)
order_items_df.to_parquet('order_items.parquet', index=False)

print("Data generation complete.")
