# ask to aske bot
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def getting_chunks_pdf():
    pdfs_directory = os.path.join(BASE_DIR, 'media/pdfs')
    pdf_loader = PyPDFDirectoryLoader(pdfs_directory)
    data = pdf_loader.load()
    print("Number of PDFs loaded:", len(data))  # Debugging line
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    text_chunks = text_splitter.split_documents(data)
    print("Number of text chunks:", len(text_chunks))  # Debugging line
    return text_chunks
