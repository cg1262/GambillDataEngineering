import anthropic
import pandas as pd
import pyodbc
import json
from io import StringIO
import GetParameters as gp
import openai
from datetime import datetime
# Set your parameter file path
local_param_file = 'D:/data/params.txt'  # Replace with the location of your parameter file
# Retrieve your OpenAI and SQL Server details from the parameter file
OpenAI_key = gp.getParam(local_param_file, 'openAI_Key')
server = gp.getParam(local_param_file, 'SQL_Server')
username = gp.getParam(local_param_file, 'SQL_User')
database = gp.getParam(local_param_file, 'SQL_DB')
password = gp.getParam(local_param_file, 'SQL_PW')
claude_key = gp.getParam(local_param_file, 'claude_key')
# ... (keep the previous imports and client initialization)
# Initialize Anthropic client


def choose_ai(prompt,ai_name):
    if ai_name.lower() == 'openai':
        api_key = OpenAI_key
        client = openai.api_key = api_key
        response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",  # Or use "gpt-4" if available
                    messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that generates synthetic dataset schemas."},
                    {"role": "user", "content": prompt}
                    ],
                    max_tokens=4096
                    )
    elif ai_name.lower() == 'anthropic':
        api_key = claude_key
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=4096,
                    temperature=0.7,
                    system="You are a helpful AI assistant that generates synthetic dataset schemas.",
                    messages=[{"role": "user", "content": prompt}]
                    )
    return response

def generate_synthetic_schema(description, custom_columns, constraints,ai_name):
    prompt = f"""
    Generate a synthetic dataset schema.
    Data should mimic {description}.
    Provide the schema as a JSON object with a 'columns' key containing an array of column objects.
    Each column object should have 'name' and 'type' keys.
    Only return the JSON object, no other text.
    """   
    if custom_columns:
        prompt += f" In addition to the columns you suggest, it should also include these columns: {custom_columns}."
    if constraints:
        prompt += f" Constraints: {constraints}."

    response = choose_ai(prompt,ai_name)
    
    
    """client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=3000,
        temperature=0.7,
        system="You are a helpful AI assistant that generates synthetic dataset schemas.",
        messages=[{"role": "user", "content": prompt}]
    )
    """
    # Parse the JSON response
    if ai_choice.lower() == 'openai':
        data =  response['choices'][0]['message']['content'] 
    elif ai_choice.lower() == 'anthropic':
        data = response.content[0].text  
    try:
        if ai_choice.lower() == 'openai':
            schema = json.loads(data)
        elif ai_choice.lower() == 'anthropic':
            schema = json.loads(data)
        #print("Generated schema:", json.dumps(schema, indent=2))
        return schema
    except json.JSONDecodeError:
        print("Error: Unable to parse schema JSON. Raw response:", data)
        return None

def generate_synthetic_data_batch(schema, batch_size, description, custom_columns, constraints,query,ai_name):
    column_names = [col['name'] for col in schema['columns']]
    prompt = f"""
    Generate a synthetic dataset with exactly {batch_size} records.
    Data should mimic {description}.
    Use these column names: {', '.join(column_names)}
    Provide the data as a insert into statement for sql.
    Please return the insert statements with the values needed to be inserted into this table format:
    {query}
    Only return the insert statements separated by a semicolon with one on each row as text and not any markdown. 
    If there is a value with an apostrophe in it please replace it with: ''. Please NOT IN MARKDOWN!
    """ # as text and not any markdown
    if constraints:
        prompt += f" Constraints: {constraints}."

    response = choose_ai(prompt,ai_name)
    try: 
        if ai_choice.lower() == 'openai':
            data = response['choices'][0]['message']['content'] 
        elif ai_choice.lower() == 'anthropic':
            data = response.content[0].text 
        #print(data)
    except Exception as e:
        print(e)
        print(data)
    return data 

def load_data_to_sql_server(data, table_name, connection_string):
    # Create a DataFrame from the CSV data
    #df = pd.read_csv(StringIO(data))
    #print(data)
    # Establish a connection to SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(data)
    # Create the table (adjust datatypes as needed)
    #columns = [f"{col} NVARCHAR(255)" for col in df.columns]
    #create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
    #cursor.execute(create_table_query)

    # Insert the data
    
    """
    for _, row in df.iterrows():
        placeholders = ', '.join(['?' for _ in row])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        print(tuple(row))
        print(insert_query)
        try:
            cursor.execute(insert_query, tuple(row))
        except Exception as e:
            print(f"Could not load:")
            print(insert_query)
            print(e)
    """
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_table_if_not_exists(table_name, schema, connection_string):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    columns = [col['name'].replace(' ','_') + " NVARCHAR(max)" for col in schema['columns']]
    create_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
    create_table_query = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U') CREATE TABLE {table_name} ({', '.join(columns)})"
    
    print(create_table_query)
    try: 
        cursor.execute(create_table_query)
    except: 
        cursor.execute(f"DROP TABLE {table_name}")
        cursor.execute(create_table_query)
    
    conn.commit()
    conn.close()
    return create_query

def generate_and_load_data(schema, total_records, batch_size, table_name, connection_string, description, custom_columns, constraints,ai_name):
    if schema is None:
        print("Error: Invalid schema. Cannot proceed.")
        return

    query = create_table_if_not_exists(table_name, schema, connection_string)
    
    records_generated = 0
    while records_generated < total_records:
        current_batch_size = min(batch_size, total_records - records_generated)
        synthetic_data = generate_synthetic_data_batch(schema, current_batch_size, description, custom_columns, constraints,query,ai_name)
        load_data_to_sql_server(synthetic_data, table_name, connection_string)
        records_generated += current_batch_size
        print(f"Generated and loaded {records_generated} records so far...")

    print(f"Successfully loaded {records_generated} records into {table_name}")

# Example usage
description = 'Blue Cross Blue Shield Healthcare claims.'
custom_columns = ''
constraints = ''
total_records = 500
batch_size = 10
ai_choice = 'OpenAI' #OpenAI or Anthropic
table_name = f"staging.BCBS_{ai_choice}"
schema = generate_synthetic_schema(description, custom_columns, constraints,ai_choice)
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
start_time = datetime.now()
generate_and_load_data(schema, total_records, batch_size, table_name, conn_str, description, custom_columns, constraints,ai_choice)
end_time = datetime.now()
difference = end_time - start_time
print(ai_choice,"Seconds:", difference.seconds)