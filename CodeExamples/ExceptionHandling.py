import sys 

def check_age(age):
    age = int(age)
     
    if age < 18:
        raise ValueError('Age must be 18 or older.')

    return True
    
check_age(input("Please Enter Your Age: "))