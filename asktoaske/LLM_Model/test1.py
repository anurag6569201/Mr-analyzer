from asyncio.log import logger
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
import os
from langchain.prompts import PromptTemplate
from analyzer.asktoaske_hugging import text_split

#download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

embeddings = download_hugging_face_embeddings()


#Initializing the Pinecone
def initialize_pinecone(text_chunks):
    import os
    from pinecone import Pinecone
    pinecone_api=os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api)
    index = pc.Index("mr-analyzer")
    index_name="mr-analyzer"
    index.delete(delete_all=True)

    from langchain.vectorstores import Pinecone as PC
    docs_chunks = [t.page_content for t in text_chunks]
    pinecone_index = PC.from_texts(
        docs_chunks,
        embeddings,
        index_name='mr-analyzer'
    )

def load_alredy_index():
    from langchain.vectorstores import Pinecone as PC
    index_name="mr-analyzer"
    docsearch=PC.from_existing_index(index_name, embeddings)
    return docsearch

prompt_template="""
You are a seasoned Q&A expert. Based on the context provided, your task is to give a clear and concise answer. Add a dash of humor and drama with a playful question at the end, but only about 35% of the time. 🌟 

Context: {context}
Question: {question}

If you dont know the answer, simply state that you dont know—no need to guess.
Helpful answer:
"""

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}


from langchain_google_genai import ChatGoogleGenerativeAI
google_gemini_api=os.getenv("GOOGLE_API_KEY")
llm_model=ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=google_gemini_api)

qa=RetrievalQA.from_chain_type(
    llm=llm_model, 
    chain_type="stuff",
    retriever=load_alredy_index().as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)

# while True:
#     user_input=input(f"Input Prompt:")
#     result=qa({"query": user_input})
#     print("Response : ", result["result"])

def get_response(query):
    user_input = query
    try:
        result=qa({"query": user_input})
        return result["result"]
    except Exception as e:
        logger.error(f"Error while getting response: {e}")
        return "Sorry, I couldn't process your request."
