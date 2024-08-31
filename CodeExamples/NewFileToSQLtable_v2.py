import pandas as pd
import sqlalchemy as sa
import pyodbc
import json
import logging
import os
# Configure logging
logging.basicConfig(filename='data_load.log', level=logging.INFO)

def load_data(file_path, table_name, connection_string):
    """
    Reads a CSV or JSON file, infers the schema, creates a table in the staging schema, and loads the data.

    Args:
        file_path (str): The path to the CSV or JSON file.
        table_name (str): The desired name of the table in the staging schema.
        connection_string (str): The connection string to the SQL Server database.
    """

    # Connect to SQL Server
    engine = sa.create_engine(connection_string)
    conn = engine.connect()

    # Infer the schema based on file type
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.json_normalize(data)
    else:
        raise ValueError("Unsupported file format.")

    # Use SQLAlchemy to infer data types from DataFrame
    data_types = sa.types.infer_column_types(df.to_sql(name="temp", con=engine, index=False))

    # Create SQL table definition
    column_defs = ", ".join(f"[{col}] {data_types[col]}" for col in df.columns)
    create_table_sql = f"""
    CREATE TABLE staging.{table_name} (
        {column_defs}
    )
    """

    try:
        # Check if table exists and drop only if required
        if engine.dialect.has_table(engine, "staging", table_name):
            logging.info(f"Table 'staging.{table_name}' already exists. Skipping creation.")
        else:
            logging.info(f"Creating table 'staging.{table_name}'...")
            conn.execute(create_table_sql)

        # Load data using pandas.to_sql with chunking
        logging.info(f"Loading data into 'staging.{table_name}'...")
        df.to_sql(f"staging.{table_name}", con=engine, index=False, if_exists="append", chunksize=1000)

        logging.info("Data loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    # Use environment variables or a secure configuration file for credentials
    connection_string = f"mssql+pyodbc://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_SERVER']}/{os.environ['DB_NAME']}?driver=ODBC+Driver+17+for+SQL+Server"
    file_path = "D:/data/netflix/Netflix_Userbase.csv"  # Replace with your file path
    table_name = "Netflix"  # Replace with your desired table name
    load_data(file_path, table_name, connection_string)