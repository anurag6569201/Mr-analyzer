from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


#Create text chunks
def text_split():
    pdfs_directory = os.path.join(BASE_DIR, 'media/pdfs')
    loader = DirectoryLoader(pdfs_directory,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    documents = loader.load()
    extracted_data = documents

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks
