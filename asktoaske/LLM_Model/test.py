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

# Load and prepare data
def prepare_vector_store(persist_directory="db"):
    text_chunks=getting_chunks_pdf()
    embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectordb = Chroma.from_documents(
        documents=text_chunks,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever()
    return retriever

# Create the question-answering chain
def create_chain():
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
    retriever = prepare_vector_store()
    chain = create_retrieval_chain(retriever, question_answer_chain)
    return chain

def get_response(query):
    chain = create_chain()
    response = chain.invoke({"input": query})
    return response.get('answer', '')
