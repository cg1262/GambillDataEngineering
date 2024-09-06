"""
# Creating a list
fruits = ['apple', 'banana', 'cherry']

fruit2 = ['grape','pear','strawberry']
# Accessing elements
print(fruits[0])  # Output: apple

# Adding an element
fruits.append('orange')

# Removing an element
fruits.remove('banana')

# Modifying an element
fruits[1] = 'blueberry'
for f in fruit2:
    fruits.append(f)
    
for fruit in fruits:
    print(fruit)

print(fruits)
"""
"""
# Creating a dictionary
student = {
    'name': 'John',
    'age': 21,
    'courses': ['Math', 'Computer Science']
}
print(student.keys())
print(student.items())

for key,value in student.items():
    if key == 'name':
        stud = value 
        for item in student['courses']:
            print(f'{stud} is registered in {item} course.')
            
student['address']= '123 Happy Ln'
print(student)

list_of_dictionaries = []
list_of_dictionaries.append(student)
student2 = {
    'name': 'Chris',
    'age': 19,
    'courses': ['English','Math', 'Computer Science'],
    'address': '154 Sad St.'
}
list_of_dictionaries.append(student2)
for record in list_of_dictionaries:
    print(f"Name: {record['name']}, Courses: {', '.join(record['courses'])}") #we will talk about the join function in a future course... 




# Accessing values
print(student['name'])  # Output: John

# Adding a new key-value pair
student['grade'] = 'A'

# Modifying a value
student['age'] = 22

# Removing a key-value pair
del student['courses']
print(student)
"""
"""""""""
print("***CREATING A SET ***")
# Creating a set
colors = {'red', 'green', 'blue'}

# Adding an element
colors.add('yellow')

# Removing an element
colors.discard('green')

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# Union
print(set1 | set2)  # Output: {1, 2, 3, 4, 5}

# Intersection
print(set1 & set2)  # Output: {3}

# Difference
print(set1 - set2)  # Output: {1, 2}

"""
# Creating a tuple
dimensions = (1920, 1080)

# Accessing elements
print(dimensions[0])  # Output: 1920

# Tuples can be used as keys in dictionaries
locations = {
    (35.6895, 139.6917): 'Tokyo',
    (40.7128, -74.0060): 'New York'
}
print(locations)
# Tuple unpacking
width, height = dimensions
print(f'Width: {width}, Height: {height}')  # Output: Width: 1920, Height: 1080
