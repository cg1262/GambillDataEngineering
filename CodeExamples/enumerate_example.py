names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 88]

for name, score in zip(names, scores):
    print(f'{name} scored {score}')

combined = list(zip(names,scores))
print(combined)