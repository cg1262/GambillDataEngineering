import GetParameters as gp

def greet(name):
    return f"Hello, {name}!"



local_param_file = 'D:/data/params.txt'

hello = gp.getParam(local_param_file,'Hello')

add_numbers = gp.add(6,10)

sub_numbers = gp.subtract(10,6)

print(greet("Chris"))

print(f'6+10 = {add_numbers}')

print(f'10-6 = {sub_numbers}')

print(hello)
