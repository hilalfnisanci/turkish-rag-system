import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
import os

class DocumentProcessor:
    """Process PDF and TXT documents into chunks"""
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " "]
        )
    
    def process_pdf(self, file_path: str):
        """Process PDF file and return chunks"""
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            chunks = self.splitter.split_documents(documents)
            
            # Add metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["source"] = file_path
                chunk.metadata["chunk_id"] = i
            
            return chunks
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return []
    
    def process_text(self, file_path: str):
        """Process TXT file and return chunks"""
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
            chunks = self.splitter.split_documents(documents)
            
            # Add metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["source"] = file_path
                chunk.metadata["chunk_id"] = i
            
            return chunks
        except Exception as e:
            print(f"Error processing TXT {file_path}: {e}")
            return []