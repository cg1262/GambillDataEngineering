# Import New data into staging tables
import pandas as pd
import sqlalchemy as sa
import pyodbc
import json
import sys

def load_data(file_path, table_name):
    """
    Reads a CSV or JSON file, infers the schema, creates a table in the staging schema, and loads the data.
    """

    # Connect to SQL Server
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
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        elif file_path.endswith(".parquet"):
            df = pd.read_parquet(file_path)
        else:
            raise ValueError("Unsupported file format.")

        # Map Pandas data types to SQL Server data types
        data_type_map = {
            'object': 'nvarchar(max)',
            'int64': 'bigint',
            'int32': 'int',
            'float64': 'float',
            'bool': 'bit',
            'datetime64[ns]': 'datetime2',
        }

        column_defs = ", ".join(
            f"[{col}] {data_type_map.get(str(dtype), 'nvarchar(max)')}" for col, dtype in df.dtypes.items()
        )

        create_table_sql = f"""
        IF OBJECT_ID('staging.{table_name}', 'U') IS NOT NULL
            DROP TABLE staging.{table_name};
        CREATE TABLE staging.{table_name} (
            {column_defs}
        )
        """

        # Execute SQL statements
        cursor.execute(create_table_sql)
        conn.commit()

        # Use df.to_sql() for efficient bulk insert
        df.to_sql(
            name=table_name,
            con=engine,
            schema='staging',
            if_exists='append',
            index=False,
            method='multi'  # Use 'multi' for batch insert
        )

        print(f"Data loaded successfully into staging.{table_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    newFile = sys.argv[5]
    newTable = sys.argv[6]
    load_data(newFile, newTable)
