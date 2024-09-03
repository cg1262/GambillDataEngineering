
def getParam(ParameterFile,ParameterName):
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
    print(f"param1: {parameterValue}")
    return parameterValue
 
