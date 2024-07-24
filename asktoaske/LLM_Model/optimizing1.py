import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
# ask to aske bot
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def getting_chunks_pdf():
    pdf_loader=PyPDFDirectoryLoader("pdfs")
    data = pdf_loader.load()
    print("Number of PDFs loaded:", len(data))  # Debugging line
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    text_chunks = text_splitter.split_documents(data)
    print("Number of text chunks:", len(text_chunks))  # Debugging line
    return text_chunks
# Load environment variables
load_dotenv()
google_gemini_api = os.getenv("GOOGLE_API_KEY")

# Initialize global variables for reusability
text_chunks = getting_chunks_pdf()
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
persist_directory = "db"

def get_vector_store():
    start_time = time.time()
    if not os.path.exists(persist_directory):
        vectordb = Chroma.from_documents(
            documents=text_chunks,
            embedding=embedding,
            persist_directory=persist_directory
        )
        vectordb.persist()
    else:
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    end_time = time.time()
    print(f"Time to get vector store: {end_time - start_time} seconds")
    return vectordb

def get_retriever():
    start_time = time.time()
    vectordb = get_vector_store()
    retriever = vectordb.as_retriever()
    end_time = time.time()
    print(f"Time to get retriever: {end_time - start_time} seconds")
    return retriever

def get_chain():
    start_time = time.time()
    system_prompt = (
        "You are an expert in question and answering. Given the following context, it is your job to provide a useful and concise answer. "
        "Make sure to ask a follow-up question in a dramatic and funny way at the end to make the interaction engaging and a bit humorous, funny, and naughty, but only where it seems appropriate. "
        "Use emojis. "
        "Context: {context}"
    )
    llm_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_gemini_api)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm_model, prompt)
    retriever = get_retriever()
    chain = create_retrieval_chain(retriever, question_answer_chain)
    end_time = time.time()
    print(f"Time to create chain: {end_time - start_time} seconds")
    return chain

def get_response(query):
    start_time = time.time()
    chain = get_chain()
    response = chain.invoke({"input": query})
    end_time = time.time()
    print(f"Time to get response: {end_time - start_time} seconds")
    return response.get('answer', '')

query="is anurag can be a developer"
resp=get_response(query)
print(resp)
print("----------------------------")

query="is anurag have python knowledge?"
resp=get_response(query)
print(resp)
print("----------------------------")