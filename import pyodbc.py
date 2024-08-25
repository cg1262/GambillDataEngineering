from sqlalchemy import create_engine
import urllib
import pyodbc
import pandas as pd

quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=GAMBILL-ALIEN-2;DATABASE=DEV-GDE")
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

local_file = "D:/Data/sales_data_sample.xlsx"
 
df = pd.read_excel(local_file)
df.to_sql("SALES_DATA",schema="STAGING",con=engine)