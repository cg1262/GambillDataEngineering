
numbers = [1, 2, 3, 4, 5]
squared = [num * num for num in numbers]
print(squared)  # Output: [1, 4, 9, 16, 25]

evens = [num for num in numbers if num % 2 == 0]
print(evens)  # Output: [2, 4]

names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 88]

for name, score in zip(names, scores):
    print(f'{name} scored {score}')

for index, name in enumerate(names):
    print(f'{index}: {name}')

large_numbers = (num * num for num in range(1, 1000000))
print(next(large_numbers))  # Output: 1
print(next(large_numbers))  # Output: 4

matrix1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

matrix2 = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
]

# Initialize result matrix with zeros
result_matrix = [
    [0 for _ in range(len(matrix1[0]))]
    for _ in range(len(matrix1))
]

for i in range(len(matrix1)):
    for j in range(len(matrix1[0])):
        result_matrix[i][j] = matrix1[i][j] + matrix2[i][j]

print("Sum of matrices:")
for row in result_matrix:
    print(row)

result_matrix = [
    [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
    for i in range(len(matrix1))
]

print("Sum of matrices with list comprehension:")
for row in result_matrix:
    print(row)
