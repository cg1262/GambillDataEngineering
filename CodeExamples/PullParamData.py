

# Create an empty dictionary to store parameters
params = {}

# Open the parameter file and read it line by line
with open('D:/data/params.txt', 'r') as file:
    for line in file:
        # Strip any whitespace and split the line by the '=' character
        key, value = line.strip().split('=')
        # Store the key-value pair in the dictionary
        params[key] = value

# Now you can access your parameters as variables
OpenAI_Key = params['openAI_Key']
SQL_Server = params['SQL_Server']
SQL_DataBase = params['SQL_DB']

# Print the variables to verify
print(f"param1: {OpenAI_Key}")
print(f"param2: {SQL_Server}")
print(f"param3: {SQL_DataBase}")
