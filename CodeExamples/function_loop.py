import pandas as pd

# Sample data with duplicates
data = {
    'id': [1, 1, 2, 3, 3, 4],
    'name': ['apple', 'apple', 'banana', 'cherry', 'cherry', 'orange'],
    'price': [1.25, 1.25, 2.50, 3.00, 3.00, 4.00]
}

df = pd.DataFrame(data)

# Function to remove duplicates (using a set for efficient membership checking)
def remove_duplicates(df):
  unique_rows = set(df.to_records(index=False).tolist())
  return pd.DataFrame(list(unique_rows), columns=df.columns)

# Remove duplicates
df_unique = remove_duplicates(df.copy())
print("Original data with duplicates:")
print(df)
print("\nData after removing duplicates:")
print(df_unique)

# Function to create a new feature (discount based on price)
def create_new_feature(df):
  for index, row in df.iterrows():
    price = row['price']
    discount = 0.1 if price > 2.0 else 0.05
    df.loc[index, 'discount'] = discount
    df.loc[index, 'new_price'] = round(price - discount * price,2)
  return df

# Create a new 'discount' feature
df_with_discount = create_new_feature(df.copy())
print("\nOriginal data:")
print(df)
print("\nData with new 'discount' feature:")
print(df_with_discount)