import time
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT, AnthropicBedrock
import GetParameters as gp

# Set your parameter file path
local_param_file = 'D:/data/params.txt'  # Replace with the location of your parameter file
# Retrieve your OpenAI and SQL Server details from the parameter file
OpenAI_key = gp.getParam(local_param_file, 'openAI_Key')
server = gp.getParam(local_param_file, 'SQL_Server')
username = gp.getParam(local_param_file, 'SQL_User')
database = gp.getParam(local_param_file, 'SQL_DB')
password = gp.getParam(local_param_file, 'SQL_PW')
claude_key = gp.getParam(local_param_file, 'claude_key')
# Set OpenAI API Key
openai.api_key = OpenAI_key

anthropic = Anthropic(api_key=claude_key)

def generate_openai(prompt):
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Or use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a Director of Data with 25 years of experience in data engineering."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )
    end_time = time.time()
    return response['choices'][0]['message']['content'], end_time - start_time

def generate_claude(prompt):
    start_time = time.time()
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[
            
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )
    end_time = time.time()
    return response.content, end_time - start_time

def compare_models(prompt):
    openai_response, openai_time = generate_openai(prompt)
    claude_response, claude_time = generate_claude(prompt)

    print(f"OpenAI response: {openai_response}")
    print(f"OpenAI time: {openai_time:.2f} seconds")
    print(f"\nClaude response: {claude_response}")
    print(f"Claude time: {claude_time:.2f} seconds")

# Example usage
niche = 'Data Engineering'
social_platform = 'YouTube'
target_audience = 'SMBs and aspiring data engineers starting their data journey.'
prompt = f"""
You are an expert social media strategist for the niche of {niche}. 
Provide a month's worth of content ideas for {social_platform} that are engaging relevant
and tailored to {target_audience} within this niche. 
The ideas should include a specific topic related to the niche and consider trending
topics and seasonal relevance to maximize engagement. 
present the ideas with the
following fields: platform, idea, description, topic, title, video description,
audience appeal, outline and hook. 
Ensure that ideas cater to diverse audience preferences within 
the niche and are varied to keep the content fresh and interesting.
Response should be a json payload with the fields being proper case and with underscores in fields between words.
"""

#prompt = "Provide a table formatted list of 10 content ideals for a youtube channel called The Data Engineering channel that focuses on providing training for aspiring data professionals." 
#Provide a synthetic dataset of 10 rows containing data from SquareEnix's MMO subscriber list.
compare_models(prompt)