import requests
import polars as pl
from sqlalchemy import create_engine
import urllib
import pyodbc
import pandas as pd

quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=GAMBILL-ALIEN-2;DATABASE=DEV-GDE")
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

api_key = 'Api key here'
currency_type = 'usd'

Endpoint_URL = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency_type}"
headers = {"accept": "application/json"}
Body = {"x-cg-demo-api-key":{api_key}}

response = requests.get(Endpoint_URL, headers=headers,data=Body) 
print("------------------------------------------")
print("Status:")
print(response.status_code)
print("------------------------------------------")
print("Header:")
print(response.headers)
print("------------------------------------------")
print("Body:")
print(response.text)

#df = pl.DataFrame(response.json())
#df.write_excel("D:/Data/cryptoCG.xlsx")
 
