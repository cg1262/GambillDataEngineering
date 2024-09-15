import pandas as pd


file_name = ["customers","order_items",'orders']

for file in file_name:
    df = pd.read_parquet(f"D:/{file}.parquet")
    df.to_csv(f"D:/{file}.csv","|",index=False)