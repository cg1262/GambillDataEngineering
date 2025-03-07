import requests  # this is the library to pull api data
from datetime import datetime # this library does all things datetime
import hashlib  #this library can create hashes
import ssl  #this library works with ssl 
import polars as pl #this library is similar to pandas below but also has some spark and parallism to it
import json  #this library works with json data
import pandas as pd #this library is going to be one of librarys you use the most as a DE
import pyodbc #this library allows you to make connections to databases 
#import sqlalchemy 

#variables  
#all_comics = []
#all_characters = []
limit = 10
offset = 0
marvel_pub_key = 'c65cab93e25935495c4d6643d58198b3'
self_private_key = 'c8c38fe6387c2aad4400be3cb0eacd7dadcc52ec'
displayInYT = '"Data provided by Marvel. © 2014 Marvel"'
attribution_notice_link = 'http://marvel.com'
v_TimeStamp = datetime.now()
str_TimeStamp = datetime.strftime(v_TimeStamp,'%Y-%m-%d %H:%M:%S')
base_api = 'https://gateway.marvel.com/v1/public/'
db_dsn = 'GDE_dev'
ConnectionString = f'DSN={db_dsn}'
connection_string = f'mssql+pyodbc://{db_dsn}'
#engine = sqlalchemy.create_engine(connection_string)
#class to adjust TSL for SSL
class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("AES128-SHA256")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

 
#function to generate md5 has for request
def generate_md5_hash(input_string):
    # Create an md5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the digest
    hash_result = md5_hash.hexdigest()

    return hash_result

#def createConnection(ConnectionString):
conn = pyodbc.connect(ConnectionString)
cursor = conn.cursor()
#    return cursor 

#db_cur = createConnection(f'DSN={db_dsn}')

v_md5hash = generate_md5_hash(str_TimeStamp+self_private_key+marvel_pub_key)
#print(v_md5hash)
resource_name = ''


#print(req_api)
def get_data(req_api,limit,offset):
    params = {
    # 'apikey': api_key,
    'limit': limit,
    'offset': offset
    }
    req_api = f'{req_api}&limit={limit}&offset={offset}'
    try:
        with requests.session() as s:
            s.mount("https://", TLSAdapter())
            response = s.get(req_api) #,params=params
            print(response.status_code)
        return response.json()
            #print(s.get(req_api))
    except Exception as e: 
        print(e)
        return None

resource_name = 'comics'
extended_URI = f'?ts={str_TimeStamp}&apikey={marvel_pub_key}&hash={v_md5hash}'
req_api =f'{base_api}{resource_name}?ts={str_TimeStamp}&apikey={marvel_pub_key}&hash={v_md5hash}'
comics = get_data(req_api=req_api,limit=limit,offset=offset)
comic_list = comics["data"]["results"]
#print(comic_list)

for comic in comic_list:
    """    print(comic["title"])#["title"]
    print(f'{comic["images"][0]["path"]}.{comic["images"][0]["extension"]}')"""
    print(comic["title"])
    print("_______________________________________________")
    char = get_data(f'{comic["characters"]["collectionURI"]}{extended_URI}',20,0)
    print(char)
    print("_______________________________________________")