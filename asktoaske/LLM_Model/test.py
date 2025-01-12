import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from analyzer.asktoaske_utils import getting_chunks_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
google_gemini_api = os.getenv("GOOGLE_API_KEY")

# Initialize global variables for reusability
text_chunks = getting_chunks_pdf()
print(text_chunks)
embedding_models = [
    GoogleGenerativeAIEmbeddings(model="models/embedding-001")
]
llm_models = [
    ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv('GOOGLE_API_KEY'))
]
persist_directory = "db"

# Basic memory class
class Memory:
    def __init__(self):
        self.history = []

    def add(self, entry):
        self.history.append(entry)
        if len(self.history) > 10:  # Limit the history size
            self.history.pop(0)

    def get_context(self):
        return " ".join(self.history)

memory = Memory()

def get_vector_store(embedding):
    try:
        if not os.path.exists(persist_directory):
            vectordb = Chroma.from_documents(
                documents=text_chunks,
                embedding=embedding,
                persist_directory=persist_directory
            )
            vectordb.persist()
            logger.info("Vector store created and persisted.")
        else:
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
            logger.info("Loaded existing vector store.")
        return vectordb
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise

def get_retriever():
    for embedding in embedding_models:
        try:
            vectordb = get_vector_store(embedding)
            return vectordb.as_retriever()
        except Exception as e:
            logger.error(f"Error with embedding model {embedding.model}: {e}")
    raise RuntimeError("All embedding models failed")

def get_chain():
    system_prompt = (
        "You are an expert in question and answering. Given the following context, it is your job to provide a useful and concise answer. "
        "Make sure to ask a follow-up question in a dramatic and funny way at the end to make the interaction engaging and a bit humorous, but only where it seems appropriate. "
        "Use emojis. "
        "Context: {context}"
    )
    
    for llm_model in llm_models:
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}"),
                ]
            )
            question_answer_chain = create_stuff_documents_chain(llm_model, prompt)
            retriever = get_retriever()
            chain = create_retrieval_chain(retriever, question_answer_chain)
            logger.info("Question-answering chain created successfully.")
            return chain
        except Exception as e:
            logger.error(f"Error with LLM model {llm_model.model}: {e}")
    raise RuntimeError("All LLM models failed")

def get_response(query):
    chain = get_chain()
    try:
        context = memory.get_context()
        response = chain.invoke({"input": query, "context": context})
        answer = response.get('answer', '')
        # Add query and answer to memory
        memory.add(f"User: {query}\nAI: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error while getting response: {e}")
        return "Sorry, I couldn't process your request."

