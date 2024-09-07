import re
import openai
import pyodbc
import GetParameters as gp
import json

# Function to create SQL column definitions from JSON
def parse_json_response(json_response):
    columns = json_response["columns"]
    data = json_response["data"]
    sql = json_response['sql_create']
    # Create SQL column definitions
    columns_with_types = [f"{col['name']} {col['type']}" for col in columns]
    create_table_structure = ", ".join(columns_with_types)

    return create_table_structure, data, sql

# Function to extract and clean JSON content from the response (handles Markdown)
def extract_json_from_response(response_text):
    # Use regex to find JSON wrapped in Markdown (```json ... ```)
    json_match = re.search(r'```json(.*?)```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()  # Extract and strip whitespace
        return json_str
    else:
        # Fallback to return the response as-is if no Markdown is found
        return response_text

# Set your parameter file path
local_param_file = 'D:/data/params.txt'  # Replace with the location of your parameter file

# Retrieve your OpenAI and SQL Server details from the parameter file
OpenAI_key = gp.getParam(local_param_file, 'openAI_Key')
server = gp.getParam(local_param_file, 'SQL_Server')
username = gp.getParam(local_param_file, 'SQL_User')
database = gp.getParam(local_param_file, 'SQL_DB')
password = gp.getParam(local_param_file, 'SQL_PW')

# Set OpenAI API Key
openai.api_key = OpenAI_key

# 1. Get user input for dataset generation
dataset_description = input("Describe the type of dataset you want (e.g., 'marketing data from a large corporate firm similar to Coca-Cola'): ")
total_rows = int(input("Enter the number of rows: "))
batch_size = 50  # Specify the batch size (adjust as needed to fit within token limits)

# Optional: Custom columns and constraints
custom_columns = input("Do you want to specify custom columns? (e.g., 'id, name, sales_amount', leave blank for none): ")
constraints = input("Any special constraints (e.g., 'include primary key, no null values', leave blank for none): ")
table_name = input("What should your Table be named (include schema): ")

# Function to request dataset in batches
def request_dataset_in_batches(dataset_description, batch_size, start_row, custom_columns, constraints, table_name):
    prompt = f'''
    Generate a dataset of {batch_size} rows of {dataset_description} starting from row {start_row} in JSON format.
    The JSON response should include:
    1. A "columns" section where each column is defined with its name and data type.
    2. A "data" section that contains exactly {batch_size} rows of data starting from row {start_row}.
    Ensure the number of rows matches the requested count.
    3. Ensure there are no missing values or incomplete records.
    4. A "sql_create" section with a create table SQL statement to create the table {table_name} in SQL Server.
    Return the full dataset in valid JSON format. Do not truncate or summarize the rows.
    '''

    # Add custom columns to the prompt if provided
    if custom_columns:
        prompt += f" Columns: {custom_columns}."
    if constraints:
        prompt += f" Constraints: {constraints}."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Or use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a data science firm that provides properly formatted JSON responses for synthetic datasets."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )

    generated_text = response['choices'][0]['message']['content']
    return extract_json_from_response(generated_text)  # Clean the JSON response

# 2. Loop to request the dataset in batches
all_data = []  # List to store all rows
columns_sql = None  # Store the SQL column structure
for start_row in range(0, total_rows, batch_size):
    # Request a batch of rows
    json_str = request_dataset_in_batches(dataset_description, batch_size, start_row + 1, custom_columns, constraints, table_name)
    
    # Parse the JSON response
    try:
        json_response = json.loads(json_str)  # Parse the cleaned JSON string
        if columns_sql is None:
            columns_sql, batch_data,create = parse_json_response(json_response)
        else:
            _, batch_data = parse_json_response(json_response)
        
        all_data.extend(batch_data)  # Append the batch of data to the full dataset
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from OpenAI response: {e}")
        exit()

# 3. Connect to SQL Server
try:
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
except pyodbc.Error as db_error:
    print(f"Error connecting to SQL Server: {db_error}")
    exit()

# 4. Generate and execute CREATE TABLE SQL statement
try:
    create_table_sql = create
    cursor.execute(create_table_sql)
    conn.commit()
except pyodbc.Error as sql_error:
    print(f"Error creating table: {sql_error}")
    conn.rollback()
    conn.close()
    exit()

# 5. Insert synthetic data into SQL Server
try:
    for row in all_data:
        # Extract values from the JSON row, ensuring the order matches the table schema
        values = tuple(row[col['name']] for col in json_response["columns"])
        placeholders = ', '.join('?' for _ in values)  # Create placeholders for parameterized query
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_sql, values)

    conn.commit()
    print(f"Successfully created and populated the '{table_name}' table in SQL Server.")
except pyodbc.Error as insert_error:
    print(f"Error inserting data: {insert_error}")
    conn.rollback()
finally:
    conn.close()
