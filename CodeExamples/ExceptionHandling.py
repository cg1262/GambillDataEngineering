import sys 

try:
    file = open('file.txt', 'r')
    # Perform file operations
except FileNotFoundError:
    print('File not found.')
except Exception as e:
    print(e)
finally:
    sys.exit(0)

import sys
 
try:
    value = int(input('Enter a number: '))
    result = 10 / value
except ValueError:
    print("That’s not a valid number!")
except ZeroDivisionError:
    print("Oops! You can’t divide by zero.")
    
def check_age(age):
    age = int(age)
     
    if age < 18:
        raise ValueError('Age must be 18 or older.')

    return True
    
check_age(input("Please Enter Your Age: "))

print(f"I still moved on!")