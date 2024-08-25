import requests  # this is the library to pull api data
from datetime import datetime # this library does all things datetime
import hashlib  #this library can create hashes
import ssl  #this library works with ssl  
import os 

try: 
    import pyodbc 
    print("I was installed already!")
except: 
    os.system("pip install pyodbc")
    print("I intstalled the package!")
