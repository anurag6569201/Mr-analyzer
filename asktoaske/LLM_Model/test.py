from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from analyzer.asktoaske_utils import getting_chunks_pdf

# Load environment variables
load_dotenv()
google_gemini_api = os.getenv("GOOGLE_API_KEY")

# Initialize global variables for reusability
text_chunks = getting_chunks_pdf()
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
persist_directory = "db"

# Prepare and cache the vector store
def get_vector_store():
    if not os.path.exists(persist_directory):
        vectordb = Chroma.from_documents(
            documents=text_chunks,
            embedding=embedding,
            persist_directory=persist_directory
        )
        vectordb.persist()
    else:
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb

# Initialize and cache the retriever
def get_retriever():
    vectordb = get_vector_store()
    return vectordb.as_retriever()

# Create and cache the question-answering chain
def get_chain():
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
    return chain

def get_response(query):
    chain = get_chain()
    response = chain.invoke({"input": query})
    return response.get('answer', '')
