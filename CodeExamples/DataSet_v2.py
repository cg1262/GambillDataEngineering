import re
import openai
import pyodbc
import GetParameters as gp
import json

def parse_json_response(json_response):
    print(json_response)
    try:
        columns = json_response["columns"]
        data = json_response["data"]
        sql = json_response['sql_create']
        column_count = json_response["Column_Count"]
        # Log the type and content of columns to check the structure
        print(f"Columns type: {type(columns)}")
        print(f"Columns content: {columns}")
        print(f"SQL Create statement: {sql}")

        # Check if columns is a list or a dictionary
        if isinstance(columns, list):
            # Standard expected case: columns is a list of dictionaries
            columns_with_types = [f"{col['name']} {col['type']}" for col in columns]
        elif isinstance(columns, dict):
            # Handle case where columns is a dictionary of column names and types
            columns_with_types = [f"{name} {col_type}" for name, col_type in columns.items()]
        else:
            raise TypeError(f"Unexpected 'columns' type: {type(columns)}")

        create_table_structure = ", ".join(columns_with_types)
        return create_table_structure, data, sql, column_count

    except KeyError as ke:
        print(f"KeyError: {ke} - The expected keys are not present in the JSON structure.")
        raise
    except TypeError as te:
        print(f"TypeError: {te} - Issue with the structure of the JSON data. Please check the format.")
        raise

# Function to extract and clean JSON content from the response (handles Markdown)
def extract_json_from_response(response_text):
    # Use regex to find JSON wrapped in Markdown (```json ... ```)
    json_match = re.search(r'```json(.*?)```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()  # Extract and strip whitespace
    else:
        json_str = response_text
    
    # Remove comments like "// Additional ..." that break JSON format
    json_str = re.sub(r'//.*?\n', '', json_str)  # Remove single-line comments (//)
    
    return json_str

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
    """TODO: 
        Separate create table SQL Statement request from the data request and do it as two calls to the api. Then integraete the create table result into the 
        request for the data to ensure that proper structure is maintained. 
    """
    prompt = f'''
    Generate a dataset of {batch_size} rows of {dataset_description} starting from row {start_row} in JSON format.
    The JSON response should include:
    1. A "columns" section where each column is defined with its name and data type.
    2. A "data" section that contains exactly {batch_size} rows of data starting from row {start_row}.
    Ensure the number of rows matches the requested count.
    3. Ensure there are no missing values or incomplete records.
    4. A "sql_create" section with a create table SQL statement to create the table {table_name} in SQL Server.
    5. A "Column_Count" Section.
    Return the full dataset in valid JSON format. Do not truncate or summarize the rows.
    Provide the data as a JSON payload, including a header row.
    Only return the JSON data, no other text.
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
create = None  # Store the SQL CREATE statement
for start_row in range(0, total_rows, batch_size):
    # Request a batch of rows
    json_str = request_dataset_in_batches(dataset_description, batch_size, start_row + 1, custom_columns, constraints, table_name)
    
    # Parse the JSON response
    try:
        json_response = json.loads(json_str)  # Parse the cleaned JSON string
        if columns_sql is None:
            columns_sql, batch_data, create = parse_json_response(json_response)
        else:
            _, batch_data, _ = parse_json_response(json_response)  # Unpack the values but ignore create on subsequent batches
        
        # Debugging: Print the row if the key is missing
        for row in batch_data:
            try:
                values = tuple(row[col['name']] for col in json_response["columns"])
            except KeyError as e:
                print(f"KeyError: {e} - The row causing the issue: {row}")
                raise
            all_data.append(values)  # Append each row of values
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
    create_table_sql = create  # Use the `create` statement from the first batch
    cursor.execute(create_table_sql)
    conn.commit()
except pyodbc.Error as sql_error:
    try: 
        cursor.execute(f"Drop Table {table_name}")
        create_table_sql = create  # Use the `create` statement from the first batch
        cursor.execute(create_table_sql)
        conn.commit()
    except: 
        print(f"Error creating table: {sql_error}")
        conn.rollback()
        conn.close()
        exit()

# 5. Insert synthetic data into SQL Server
try:
    for values in all_data:
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
