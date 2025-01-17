import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI


google_gemini_api=os.getenv("GOOGLE_API_KEY")

# load the llm model for query using langchain
llm_model=ChatGoogleGenerativeAI(model="gemini-1.5-pro",google_api_key=google_gemini_api)

def produce_words(prompt,sound_to_use,no_of_words):
    sound_prompt = prompt.format(sound=sound_to_use,no_of_words=no_of_words)
    response = llm_model.predict(sound_prompt)
    return response


def produce_worksheet(prompt,topic_name,no_of_sentences):
    worksheet_prompt = prompt.format(topic=topic_name, no_of_sentences=no_of_sentences)
    response = llm_model.predict(worksheet_prompt)
    return response
