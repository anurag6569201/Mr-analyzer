from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_google_genai import GoogleGenerativeAI
from .utils import TEMPLATE0,TEMPLATE1,TEMPLATE2,RESPONSE_JSON
import os
import json
import pandas as pd
from dotenv import load_dotenv

# loading env file
load_dotenv()
google_gemini_api=os.getenv("GOOGLE_API_KEY")

# loading the llm model of genai through langchain
llm_model=GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyAh5HbTtCHsO_ZWAtCtn_q5h2_Jw7tEfe8")

# created prompt templates

# paragraph generation prompt
para_generation_prompt = PromptTemplate(
    input_variables=["disease_name"],
    template=TEMPLATE0
)

# MCQs generation prompt
quiz_generation_prompt = PromptTemplate(
    input_variables=["para", "number", "disease_name", "response_json"],
    template=TEMPLATE1
)

# review genration prompt
quiz_evaluation_prompt=PromptTemplate(
    input_variables=["disease_name", "quiz"], 
    template=TEMPLATE2
)

# created chains of para generation through disease name
# then it will gnerate MCQs based on the genrated paragraph
# after that it will generate a review on the genrated MCQs

para_chain=LLMChain(llm=llm_model, prompt=para_generation_prompt, output_key="para")
quiz_chain=LLMChain(llm=llm_model, prompt=quiz_generation_prompt, output_key="quiz")
review_chain=LLMChain(llm=llm_model, prompt=quiz_evaluation_prompt, output_key="review")

generate_evaluate_chain=SequentialChain(
    chains=[para_chain,quiz_chain, review_chain], 
    input_variables=["disease_name", "number", "response_json"],
    output_variables=["para", "quiz", "review"], 
)

def getting_form(disease_name,nos):
    MCQ_NUMBERS=nos
    DISEASE_NAME=disease_name
    response = generate_evaluate_chain.invoke({
        "number": MCQ_NUMBERS,
        "disease_name": DISEASE_NAME,
        "response_json": json.dumps(RESPONSE_JSON)
    })
    new_quiz_df=pd.DataFrame([response])
    return new_quiz_df
