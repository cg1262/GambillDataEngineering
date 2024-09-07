import openai
import pyodbc
import GetParameters as gp
import json
import re
# Function to extract and clean JSON content from the response
def extract_json_from_response(response_text):
    # Use regex to extract the JSON part between ```json and ```
    json_match = re.search(r'```json(.*?)```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()  # Extract and strip whitespace
        return json_str
    else:
        raise ValueError("No valid JSON found in the response.")
    
# Function to create SQL column definitions from JSON
def parse_json_response(json_response):
    columns = json_response["columns"]
    data = json_response["data"]
    sql = json_response['sql_create']
    # Create SQL column definitions
    columns_with_types = [f"{col['name']} {col['type']}" for col in columns]
    create_table_structure = ", ".join(columns_with_types)

    return create_table_structure, data, sql

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
rows = int(input("Enter the number of rows: "))

# Optional: Custom columns and constraints
custom_columns = input("Do you want to specify custom columns? (e.g., 'id, name, sales_amount', leave blank for none): ")
constraints = input("Any special constraints (e.g., 'include primary key, no null values', leave blank for none): ")
table_name = input("What should your Table be named (include schema): ")
create_table_response = f'Please provide a associated create table script for sql server in the json payload with a field name sql_create. The table name should be {table_name}.'
json_example = {"columns": [
        {"name": "customer_id", "type": "INT"},
        {"name": "customer_name", "type": "VARCHAR(100)"},
        {"name": "purchase_amount", "type": "FLOAT"},
        {"name": "purchase_date", "type": "DATETIME"}
    ],
    "sql_create": f"Create table {table_name} (customer_id int, customer_name varchar(100), purchase_amount float, purchase_date datetime)",
    "data": [
        {"customer_id": 1, "customer_name": "John Doe", "purchase_amount": 129.99, "purchase_date": "2023-09-01 12:00:00"},
        {"customer_id": 2, "customer_name": "Jane Smith", "purchase_amount": 250.45, "purchase_date": "2023-09-02 15:30:00"},
        {"customer_id": 3, "customer_name": "Sam Brown", "purchase_amount": 75.00, "purchase_date": "2023-09-03 10:15:00"}
    ]
}
# 2. Generate synthetic data and structure with OpenAI using the new API format
prompt = f'Do not truncate or summarize the rows and Generate a {dataset_description} dataset with {rows} rows in JSON format similar to {json_example}. {create_table_response}. The JSON response should include: 1. A "columns" section where each column is defined with its name and data type. 2. A "data" section that contains exactly {rows} rows of data. Ensure the number of rows matches the requested count. 3. Every record should match the schema defined in the "columns" section. 4. A "sql_create" section with a create table sql statement to create the table in sql server. Return the response in valid JSON format. Return the full dataset in valid JSON format. Do not truncate or summarize the rows.'

# Add custom columns to the prompt if provided
if custom_columns:
    prompt += f" Columns: {custom_columns}."

# Add constraints to the prompt if provided
if constraints:
    prompt += f" Constraints: {constraints}."

# Ask for JSON structured data
prompt += " Return the column definitions and the data in JSON format with column types and sample data."

response = openai.ChatCompletion.create(
    model="gpt-4-turbo",  # Or use "gpt-4" if available
    messages=[
        {"role": "system", "content": "You are a master data engineer that provides properly formatted json responses for synthetic datasets."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=4000
)

generated_text = response['choices'][0]['message']['content']
print(generated_text)
# 3. Parse the JSON response
try:
    json_str = extract_json_from_response(generated_text)  # Extract the JSON part
    json_response = json.loads(json_str)  # Convert the response string to a Python dictionary
    columns_sql, synthetic_data, create = parse_json_response(json_response)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON from OpenAI response: {e}")
    exit()

# 4. Connect to SQL Server
try:
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
except pyodbc.Error as db_error:
    print(f"Error connecting to SQL Server: {db_error}")
    exit()

# 5. Generate and execute CREATE TABLE SQL statement
try:
    create_table_sql = create
    cursor.execute(create_table_sql)
    conn.commit()
except pyodbc.Error as sql_error:
    print(f"Error creating table: {sql_error}")
    conn.rollback()
    conn.close()
    exit()

# 6. Insert synthetic data into SQL Server
try:
    for row in synthetic_data:
        # Extract values from the JSON row, ensuring the order matches the table schema
        values = tuple(row[col['name']] for col in columns_sql ) #json_response['columns']
        placeholders = ', '.join('?' for _ in values)  # Create placeholders for parameterized query
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_sql, values)

    conn.commit()
    print("Successfully created and populated the 'marketing_data' table in SQL Server.")
except pyodbc.Error as insert_error:
    print(f"Error inserting data: {insert_error}")
    conn.rollback()
finally:
    conn.close()
