import pandas as pd
import marvel_pkg as mvl
from datetime import datetime

all_comics = []
all_characters = []
limit = 100
offset = 0
marvel_pub_key = 'c65cab93e25935495c4d6643d58198b3'
self_private_key = 'c8c38fe6387c2aad4400be3cb0eacd7dadcc52ec'
api_key = "c65cab93e25935495c4d6643d58198b3"
base_url = "https://gateway.marvel.com/v1/public/"
v_TimeStamp = datetime.now()
str_TimeStamp = datetime.strftime(v_TimeStamp,'%Y-%m-%d %H:%M:%S')

v_md5hash = mvl.generate_md5_hash(str_TimeStamp+self_private_key+marvel_pub_key)
#print(v_md5hash)
req_url =f'{base_url}comics?ts={str_TimeStamp}&apikey={marvel_pub_key}&hash={v_md5hash}'
#print(req_api)
while True:
    data = mvl.fetch_data(req_url, api_key, limit, offset)
    if data is None or not data['data']['results']:
        break
    
    comics = data['data']['results']
    
    # Normalize the nested thumbnail dictionary and character data
    for comic in comics:
        comic['thumbnail_path'] = comic['thumbnail']['path']
        comic['thumbnail_extension'] = comic['thumbnail']['extension']
        
        for character in comic['characters']['items']:
            character_data = {
                'comic_id': comic['id'],
                'character_name': character['name'],
                'character_resourceURI': character['resourceURI']
            }
            all_characters.append(character_data)
    
    all_comics.extend(comics)
    offset += limit

# Convert the list of comics and characters to pandas DataFrames
df_comics = pd.DataFrame(all_comics)
df_characters = pd.DataFrame(all_characters)

# Select specific columns for the comics DataFrame
df_comics = df_comics[['id', 'digitalId', 'title', 'issueNumber', 'variantDescription', 'description', 'modified', 'isbn', 'upc', 'diamondCode', 'ean', 'issn', 'format', 'pageCount', 'resourceURI', 'thumbnail_path', 'thumbnail_extension']]

# Columns for the characters DataFrame
df_characters = df_characters[['comic_id', 'character_name', 'character_resourceURI']]

# SQL script to create the tables
create_comics_table = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='comics' and xtype='U')
CREATE TABLE staging.comics (
    id INT PRIMARY KEY,
    digitalId INT,
    title NVARCHAR(255),
    issueNumber FLOAT,
    variantDescription NVARCHAR(255),
    description NVARCHAR(MAX),
    modified DATETIME,
    isbn NVARCHAR(13),
    upc NVARCHAR(12),
    diamondCode NVARCHAR(10),
    ean NVARCHAR(13),
    issn NVARCHAR(8),
    format NVARCHAR(30),
    pageCount INT,
    resourceURI NVARCHAR(255),
    thumbnail_path NVARCHAR(255),
    thumbnail_extension NVARCHAR(10)
)
"""

create_characters_table = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='characters' and xtype='U')
CREATE TABLE staging.characters (
    comic_id INT,
    character_name NVARCHAR(255),
    character_resourceURI NVARCHAR(255),
    FOREIGN KEY (comic_id) REFERENCES comics(id)
)
"""

# Execute the SQL scripts to create the tables
mvl.cursor.execute(create_comics_table)
mvl.cursor.execute(create_characters_table)
mvl.conn.commit()

# Insert the DataFrames into the SQL Server database
df_comics.to_sql('comics', mvl.engine, if_exists='append', index=False)
df_characters.to_sql('characters', mvl.engine, if_exists='append', index=False)

# Close the cursor and connection
mvl.cursor.close()
mvl.conn.close()

print("Data inserted into the database successfully!")

