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

# Creating a tuple
dimensions = (1920, 1080)

# Accessing elements
print(dimensions[0])  # Output: 1920

# Tuples can be used as keys in dictionaries
locations = {
    (35.6895, 139.6917): 'Tokyo',
    (40.7128, -74.0060): 'New York'
}

# Tuple unpacking
width, height = dimensions
print(f'Width: {width}, Height: {height}')  # Output: Width: 1920, Height: 1080
