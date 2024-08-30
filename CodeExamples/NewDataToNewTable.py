#IMport New data into staging tables
import pandas as pd
import sqlalchemy as sa
import pyodbc
import json 
import sys

def load_data(file_path, table_name):
    """
    Reads a CSV or JSON file, infers the schema, creates a table in the staging schema, and loads the data.

    Args:
        file_path (str): The path to the CSV or JSON file.
        table_name (str): The desired name of the table in the staging schema.
    """
  
    # Connect to SQL Server
    # Pass in variables for each item in the correct order when you run the python script
    # example: NewDataToNewTable.py cgambill Password123 dev_dw IM-A-SERVER-NAME
    user = sys.argv[1]
    pw = sys.argv[2]
    db = sys.argv[3]
    server = sys.argv[4]
    
    conn_str = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={db};"
        f"UID={user};"
        f"PWD={pw};"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    engine = sa.create_engine(
        f"mssql+pyodbc://{user}:{pw}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    # Infer the schema based on file type
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.json_normalize(data)
    else:
        raise ValueError("Unsupported file format.")

    # Map Python data types to SQL Server data types
    data_type_map = {
        'object': 'nvarchar(max)',
        'int64': 'bigint',
        'int32': 'int',
        'float64': 'float',
        'bool': 'bit',
        'datetime64[ns]': 'datetime2',
    }
    itms = df.dtypes.items()
    #print(list(itms))
    # Convert data types as needed
    #df = df.astype({col: data_type_map[dtype] for col, dtype in itms})

    # Create SQL table definition -- gets appropriate data type from map and if one is not found uses varcharmax
    column_defs = ", ".join(f"[{col}] {data_type_map.get(df[col].dtype, 'nvarchar(max)')}" for col in df.columns)
    create_table_sql = f"""
    CREATE TABLE staging.{table_name} (
        {column_defs}
    )
    """
    #print(create_table_sql)
    # Execute SQL statements
    cursor.execute(f"Drop table staging.{table_name}")
    cursor.execute(create_table_sql)
    conn.commit()
    #print(df)
    # Load data into the table
    #df.to_sql(f"staging.{table_name}", con=engine, index=False,if_exists="replace")
    for index,row in df.iterrows():
        #print(row)
        sql = f"insert into staging.{table_name} VALUES("
        for col,value in row.items():
            sql = sql+f"'{value}',"
        sql = sql[:-1] + ")"
        #print(sql)
        cursor.execute(sql)
        conn.commit()
    df.to_csv("D:/data/Netflix/Testing.csv",index=False)
    #conn.commit()

    print(f"Data loaded successfully into staging.{table_name}")

if __name__ == "__main__":
    file_path = "D:/data/netflix/Netflix Userbase.csv"  # Replace with your file path
    table_name = "Netflix"  # Replace with your desired table name
    load_data(file_path, table_name)