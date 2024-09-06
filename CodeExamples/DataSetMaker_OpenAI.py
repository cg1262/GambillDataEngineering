import openai
import json
import polars as pl
import pyodbc
import GetParameters as gp

local_param_file = 'D:/data/params.txt' #replace with file of your paramaters
# Set your Variables from Paramater file
OpenAI_key = gp.getParam(local_param_file,'openAI_Key')
server = gp.getParam(local_param_file,'SQL_Server')
username = gp.getParam(local_param_file,'SQL_User')
database = gp.getParam(local_param_file,'SQL_DB')
password = gp.getParam(local_param_file,'SQL_PW')
openai.api_key = OpenAI_key
 
"""   
    prompt =  You are an expert social media strategist for the niche of {Niche}. 
    Provide a detailed list of exactly 30 viral content ideas for {SocialPlatform} that are engaging relevant
    and tailored to {TargetAudience} within this niche. 
    Each idea should include a specific topic related to the niche and consider trending
    topics and seasonal relevance to maximize engagement. 
    present the ideas in json format with the 
    following fields: idea, description, topic, youtube title, video description,
    audience appeal, outline and hook. 
    Ensure that ideas cater to diverse audience preferences within 
    the niche and are varied to keep the content fresh and interesting.
    Ensure that the content ideas are provided in a format that can be easily parsed and that all 30 ideas are included. 

"""     
def get_content_ideas_v2(target_audience, niche, social_platform, number_of_ideas,schema='',table_name=''):
    content_ideas_list = []

    for i in range(number_of_ideas):
        print(f"Requesting idea {i+1} of {number_of_ideas}...")
        prompt = f"""
        You are an expert social media strategist for the niche of {niche}. 
        Provide a content idea for {social_platform} that are engaging relevant
        and tailored to {target_audience} within this niche. 
        The idea should include a specific topic related to the niche and consider trending
        topics and seasonal relevance to maximize engagement. 
        present the ideas with the
        following fields: platform, idea, description, topic, title, video description,
        audience appeal, outline and hook. 
        Ensure that ideas cater to diverse audience preferences within 
        the niche and are varied to keep the content fresh and interesting.
        Response should be a json payload with the fields being proper case and with underscores in fields between words.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # or another model of your choice
            messages=[
                {"role": "system", "content": "You are an expert social media strategist."},
                {"role": "user", "content": prompt}
            ]
        )

        idea_content = response.choices[0].message['content']
        print(idea_content)
        # Attempt to parse the idea as JSON-like structure
        try:
            idea_json = json.loads(idea_content)
            content_ideas_list.append(idea_json)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for idea {i+1}. The content may not be in a valid JSON format.")

    # Convert list of ideas to Polars DataFrame
    df = pl.DataFrame(content_ideas_list)
    filename = f'content_ideas_{target_audience}_{niche}_{social_platform}'
    df.write_json(f"{filename}.json")
    # Save the DataFrame to a CSV file
    #csv_filename = f'content_ideas_{target_audience}_{niche}_{social_platform}.csv'
    #df.write_csv(csv_filename)
    print(df)
    #print(f"Content ideas saved to CSV file: {csv_filename}")

    # Push the data to a local SQL Server database (optional)
    if table_name != '':
        push_to_sql_server(df,schema,table_name)

def push_to_sql_server(df,schema,table_name):
    print(schema)
    print(table_name)
    # Connect to SQL Server
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};DATABASE={database};'
        f'UID={username};PWD={password}'
    )
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(f'''
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'{table_name}') AND type in (N'U'))
        CREATE TABLE {schema}.{table_name} (
            platform VARCHAR(max),
            idea VARCHAR(max),
            description VARCHAR(max),
            topic VARCHAR(max),
            title VARCHAR(max),
            video_description VARCHAR(max),
            audience_appeal VARCHAR(max),
            outline VARCHAR(max),
            hook VARCHAR(max)
        )
    ''')

    # Insert the data into the table
    for row in df.iter_rows(named=True):
         
        cursor.execute(f'''
            INSERT INTO {schema}.{table_name} 
            (platform, idea, description, topic, title, video_description, audience_appeal, outline, hook)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            social_platform,
            row['Idea'], 
            row['Description'], 
            row['Topic'], 
            row['Title'], 
            row['Video_Description'], 
            row['Audience_Appeal'], 
            json.dumps(row['Outline']),  # Convert the outline list to a JSON string
            row['Hook']
        ))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print(f"Content ideas pushed to the {schema}.{table_name} table in the SQL Server database.")

# Example usage:
target_audience = "SMBs"
niche = "data engineering"
social_platform = "TikTok"
number_of_ideas = 50  # Specify the number of content ideas you want

# Call the function to generate, save, load, and push the content ideas
get_content_ideas_v2(target_audience, niche, social_platform, number_of_ideas,'staging','content_ideas')