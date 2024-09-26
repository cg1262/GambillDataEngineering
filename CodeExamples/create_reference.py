import pandas as pd

# Create reference sheet data
data = {
    "Topic": [
        "File Handling Basics", 
        "Working with CSV Files", 
        "Handling JSON Files", 
        "Introducing Parquet Files", 
        "Using the with Statement"
    ],
    "Key Concepts": [
        "Using the open() function to read and write text files. Use 'r' for read, 'w' for write.",
        "Using the csv module to read and write CSV files. csv.reader() and csv.writer() are key functions.",
        "Using the json module to work with JSON data. json.dump() to write and json.load() to read JSON.",
        "Using pandas with pyarrow to read and write Parquet files. pandas.to_parquet() and pandas.read_parquet() are the main functions.",
        "The with statement ensures proper file closure, making file handling more efficient and less error-prone."
    ],
    "Example Code": [
        '''# Writing to a text file\nwith open('example.txt', 'w') as file:\n    file.write("Hello, world!")''',
        '''# Writing to a CSV file\nimport csv\ndata = [['Name', 'Age'], ['Chris', 30]]\nwith open('people.csv', 'w') as file:\n    writer = csv.writer(file)\n    writer.writerows(data)''',
        '''# Writing to a JSON file\nimport json\ndata = {"name": "Chris", "age": 30}\nwith open('data.json', 'w') as file:\n    json.dump(data, file)''',
        '''# Writing to a Parquet file\nimport pandas as pd\ndf = pd.DataFrame({'Name': ['Chris'], 'Age': [30]})\ndf.to_parquet('people.parquet')''',
        '''# Using with for clean file handling\nwith open('example.txt', 'r') as file:\n    content = file.read()\n    print(content)'''
    ]
}

# Create DataFrame
reference_df = pd.DataFrame(data)
print(reference_df)