import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
faker = Faker()

# Define number of records
num_customers = 10000
num_orders = 1000000
num_products = 500
num_promotions = 20

# Generate customers dataset
customers = pd.DataFrame({
    'customer_id': range(1, num_customers + 1),
    'customer_name': [faker.name() for _ in range(num_customers)]
})

# Generate products dataset
products = pd.DataFrame({
    'product_id': range(1, num_products + 1),
    'price': np.random.uniform(10, 500, num_products)
})

# Generate orders dataset
orders = pd.DataFrame({
    'order_id': range(1, num_orders + 1),
    'customer_id': np.random.choice(customers['customer_id'], num_orders),
    'order_date': [faker.date_time_this_year() for _ in range(num_orders)]
})

# Generate order details dataset
order_details = pd.DataFrame({
    'order_id': np.random.choice(orders['order_id'], num_orders * 2),
    'product_id': np.random.choice(products['product_id'], num_orders * 2),
    'quantity': np.random.randint(1, 5, num_orders * 2)
})

# Generate promotions dataset
promotions = pd.DataFrame({
    'customer_id': np.random.choice(customers['customer_id'], num_promotions),
    'discount': np.random.uniform(0.05, 0.3, num_promotions)
})

# Save datasets to CSV for user
datasets = {
    "customers.csv": customers,
    "products.csv": products,
    "orders.csv": orders,
    "order_details.csv": order_details,
    "promotions.csv": promotions
}

for filename, data in datasets.items():
    data.to_csv(f"D:/data/{filename}", index=False)

