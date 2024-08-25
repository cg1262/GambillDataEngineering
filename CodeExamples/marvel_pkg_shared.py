import pyodbc
import sqlalchemy
import requests
import hashlib  #this library can create hashes
import ssl  #this library works with ssl 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ODBC DSN name as configured on your PC
dsn_name = 'YourDSNNameHere'

# Create a connection string
connection_string = f'mssql+pyodbc://{dsn_name}'

# Create a SQLAlchemy engine
engine = sqlalchemy.create_engine(connection_string)

# Create a connection to the SQL Server database
conn = pyodbc.connect(f'DSN={dsn_name}')
cursor = conn.cursor()

# Marvel API request URL
api_key = "YourAPIKeyHere"
base_url = "https://gateway.marvel.com/v1/public/comics"
limit = 100  # Number of results per page


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("AES128-SHA256")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
    
def fetch_data(url, api_key, limit, offset):
    params = {
       # 'apikey': api_key,
        'limit': limit,
        'offset': offset
    }
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    with requests.session() as s:
        s.mount("https://", TLSAdapter())
        
    response = s.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
#function to generate md5 has for request
def generate_md5_hash(input_string):
    # Create an md5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the digest
    hash_result = md5_hash.hexdigest()

    return hash_result   


 
