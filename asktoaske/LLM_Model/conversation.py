from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.vectorstores import Chroma
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

persist_directory="db"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

google_gemini_api=os.getenv("GOOGLE_API_KEY")
llm_model=ChatGoogleGenerativeAI(model="gemini-1.5-pro",google_api_key=google_gemini_api)

system_prompt = (
    "You are an expert in question and answering. Given the following context, it is your job to provide a useful and concise answer. Make sure to ask a follow-up question in a dramatic and funny way at the end to make the interaction engaging and a bit humorous,funny and naughty, but only where it seems appropriate."
    "Use emojies"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


def getting_chunks_pdf():
    pdf_loader=PyPDFDirectoryLoader("/pdfs")
    data = pdf_loader.load()
    print("Number of PDFs loaded:", len(data))  # Debugging line
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    text_chunks = text_splitter.split_documents(data)
    print("Number of text chunks:", len(text_chunks))  # Debugging line
    return text_chunks

# creating chroma db
def creating_chroma_db(text_chunks):
    vectordb=Chroma.from_documents(
        documents=text_chunks,
        embedding=embedding,
        persist_directory=persist_directory
    )
    return vectordb

# retrive the chorma db
def getting_chroma_db(vectordb):
    vectordb.persist()
    vectordb=None
    vectordb=Chroma(persist_directory=persist_directory,embedding_function=embedding)
    retriver=vectordb.as_retriever()
    question_answer_chain = create_stuff_documents_chain(llm_model, prompt)
    chain = create_retrieval_chain(retriver, question_answer_chain)
    return chain

def askingLLM(query,finalchain):
    response=finalchain.invoke({"input": query})
    return response