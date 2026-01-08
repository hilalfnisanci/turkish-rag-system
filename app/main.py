import os
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import shutil
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA
from app.config import OPENAI_API_KEY
from app.document_processor import DocumentProcessor
from fastapi.responses import RedirectResponse

# Initialize FastAPI
app = FastAPI(title="Turkish RAG System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize ChromaDB
chroma_client = chromadb.Client()

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Initialize vectorstore
vectorstore = Chroma(
    client=chroma_client,
    embedding_function=embeddings,
    persist_directory="./data/chroma"
)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=OPENAI_API_KEY
)

# Initialize RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 3}
    ),
    return_source_documents=True
)

# Initialize document processor
processor = DocumentProcessor()

# ============ ENDPOINTS ============

@app.get("/")
async def root():
    """Redirect to frontend"""
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process PDF documents"""
    try:
        # 1. clear temporary directory
        temp_dir = "./data/temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)  
        os.makedirs(temp_dir, exist_ok=True)
        
        # 2. clear CHROMA collection
        try:
            chroma_client.delete_collection(name="langchain")
        except:
            pass
        
        # 3. create new vectorstore
        global vectorstore, qa_chain
        vectorstore = Chroma(
            client=chroma_client,
            embedding_function=embeddings,
            persist_directory="./data/chroma"
        )
        
        # 4. upload new files
        uploaded_count = 0
        for file in files:
            file_path = f"{temp_dir}/{file.filename}"
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            chunks = processor.process_pdf(file_path)
            vectorstore.add_documents(chunks)
            uploaded_count += 1
        
        # 5. update QA CHAIN
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        
        return {"status": "success", "files": uploaded_count}
    
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/ask")
async def ask_question(query: str):
    """Ask a question to the RAG system"""
    try:
        result = qa_chain({"query": query})
        return {
            "question": query,
            "answer": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/status")
async def get_status():
    """Get system status"""
    try:
        collection = chroma_client.get_or_create_collection("documents")
        return {
            "indexed_documents": collection.count(),
            "status": "ready"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}