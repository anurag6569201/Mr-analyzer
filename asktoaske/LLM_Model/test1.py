import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from asyncio.log import logger

# Download embedding model
def download_hugging_face_embeddings():
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return embedding

embeddings = download_hugging_face_embeddings()

# Initialize ChromaDB
def initialize_chromadb(text_chunks):
    persist_directory = "./chroma_db"
    vectordb = Chroma.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

# Load an already indexed ChromaDB
def load_already_indexed():
    persist_directory = "./chroma_db"
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

# Define prompt template
prompt_template = """
You are a seasoned Q&A expert. Based on the context provided, your task is to give a clear and concise answer. Add a dash of humor and drama with a playful question at the end, but only about 35% of the time. 🌟 

Context: {context}
Question: {question}

If you don't know the answer, simply state that you don't know—no need to guess.
Helpful answer:
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Initialize LLM with Google Gemini
google_gemini_api = os.getenv("GOOGLE_API_KEY")
llm_model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_gemini_api)

# Set up the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm_model,
    chain_type="stuff",
    retriever=load_already_indexed().as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

# Function to get a response
def get_response(query):
    try:
        result = qa({"query": query})
        return result["result"]
    except Exception as e:
        logger.error(f"Error while getting response: {e}")
        return "Sorry, I couldn't process your request."
