param_file = 'D:/data/params.txt'
#SQL_Password=Password

def getParam(ParameterName,ParameterFile='D:/data/params.txt'):
    # Create an empty dictionary to store parameters
    params = {}

    # Open the parameter file and read it line by line
    with open(ParameterFile, 'r') as file:
        for line in file:
            # Strip any whitespace and split the line by the '=' character
            key, value = line.strip().split('=')
            # Store the key-value pair in the dictionary
            params[key] = value

    # Now you can access your parameters as variables
    parameterValue = params[ParameterName]
 

    # Print the variables to verify
    #print(f"param1: {parameterValue}")
    return parameterValue

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y