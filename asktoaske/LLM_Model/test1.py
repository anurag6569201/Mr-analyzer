from asyncio.log import logger
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from analyzer.asktoaske_hugging import text_split

#download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

embeddings = download_hugging_face_embeddings()


# getting text chunks
text_chunks = text_split()

#Initializing the Pinecone
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

#If we already have an index we can load it like this
docsearch=PC.from_existing_index(index_name, embeddings)

query = "What anurag know in tech"

docs=docsearch.similarity_search(query, k=3)

print("Result", docs)

prompt_template="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
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
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
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
