# sample response formate
RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

# TEMPLATE0: Generate a well-researched paragraph on a disease
TEMPLATE0="""
You are an expert in medicine, specializing in the human body and various medical fields that affect human health. Your extensive knowledge encompasses a wide range of diseases, treatments, and medications. 
Your task is to write a unique, 300-word paragraph on {disease_name} . Paragraph should be well-researched, informative, and distinct from previous ones, highlighting the causes, symptoms, treatments, and any other relevant information about the disease.
"""

# TEMPLATE1: Generate a well-researched MCQ on a Given disease paragraph
TEMPLATE1="""
Text:{para}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for the disease {disease_name} for creating the public awareness. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

# TEMPLATE2: Generate a well-researched review on a Given MCQs
TEMPLATE2="""
You are an medical expert and health advocates or public health advocates. Given a Multiple Choice Quiz for {disease_name} disease.\
You need to evaluate the quality of the question and give a complete analysis of the quiz. Only use at max 50 words for quality analysis. 
if the quiz is not at per with the quality and awreness and helpfull related to the public,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the public awareness and health
Quiz_MCQs:
{quiz}

Check from an medical expert and health advocates or public health advocates of the above quiz:
"""

