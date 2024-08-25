from marvel import Marvel
import pandas as pd
marvel_pub_key = 'c65cab93e25935495c4d6643d58198b3'
self_private_key = 'c8c38fe6387c2aad4400be3cb0eacd7dadcc52ec'

m = Marvel(marvel_pub_key,self_private_key)
char = m.characters.all() 
char2 = char["data"]["results"]
#df = pd.read_json(char)
#print(df.head(10))
#df.to_csv("D:/data/marvel_characters.csv","|")
print(char2)
for c in char2:
    print(c["name"])