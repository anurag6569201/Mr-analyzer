import pandas as pd
from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

try:
    output_csv = 'static/whatsapp/temp/data.csv'
    df = pd.read_csv(output_csv)
    google_gemini_api=os.getenv("GOOGLE_API_KEY")
    llm_model=ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=google_gemini_api)
    agent = create_csv_agent(llm_model,'static/whatsapp/temp/data.csv',allow_dangerous_code=True)

except:
    print('The CSV file does not exist.')

def ask_to_csv_agent(query):
    response = agent.run(query)
    return response