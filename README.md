# 🇹🇷 Turkish RAG System

Production-ready Retrieval-Augmented Generation (RAG) system for Turkish documents.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0+-purple.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 📄 **Turkish Document Support** - PDF and TXT file processing
- 🔍 **Vector Similarity Search** - ChromaDB integration
- 🤖 **OpenAI LLM Integration** - GPT-3.5-turbo powered responses
- 🌐 **REST API** - Clean FastAPI backend
- 🎨 **Modern UI** - Simple and intuitive web interface
- 🐳 **Docker Ready** - One-command deployment

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.10+ (for local development)
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/turkish-rag-system.git
cd turkish-rag-system
```

2. **Create `.env` file**
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

3. **Run with Docker**
```bash
docker-compose up
```

4. **Open in browser**
```
http://localhost:8000/static/index.html
```

## 📖 Usage

### Upload Documents
1. Click "Choose Files" and select your Turkish PDF/TXT files
2. Click "Yükle" (Upload) button
3. Wait for "✅ uploaded" confirmation

### Ask Questions
1. Type your question in Turkish in the text area
2. Click "Soru Sor" (Ask Question)
3. Get AI-powered answers with source references

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   FastAPI    │─────▶│  ChromaDB   │
│  (HTML/JS)  │      │   Backend    │      │  (Vectors)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   OpenAI     │
                     │  GPT-3.5     │
                     └──────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Vector Database**: ChromaDB
- **LLM**: OpenAI GPT-3.5-turbo
- **Embeddings**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Document Processing**: LangChain Classic + PyPDF
- **Deployment**: Docker + Docker Compose
- **Framework**: LangChain v1.0+

## 📝 API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "ok"}
```

### Upload Documents
```bash
POST /upload
Content-Type: multipart/form-data
Body: files (PDF/TXT)
Response: {"status": "success", "files_processed": 1}
```

### Ask Question
```bash
POST /ask?query=Your+question+here
Response: {
  "question": "...",
  "answer": "...",
  "sources": [...]
}
```

### System Status
```bash
GET /status
Response: {"indexed_documents": 5, "status": "ready"}
```

## 🧪 Development

### Local Setup (without Docker)

**Requirements:**
- Python 3.10 or higher
- OpenAI API key

**Steps:**

1. **Create virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Create `.env` file**
```bash
OPENAI_API_KEY=your-api-key-here
```

4. **Run server**
```bash
python -m uvicorn app.main:app --reload
```

5. **Open browser**
```
http://localhost:8000
```

**Note:** Use `python -m uvicorn` to ensure the correct Python environment is used.

## 📁 Project Structure

```
turkish-rag-system/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   └── document_processor.py # PDF/TXT processing
├── static/
│   └── index.html           # Frontend UI
├── data/
│   ├── temp/                # Uploaded files (auto-cleared)
│   └── chroma/              # ChromaDB storage
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🎯 Roadmap

- [x] Basic RAG functionality
- [x] Turkish document support  
- [x] Docker deployment
- [x] LangChain v1.0 migration
- [x] Auto-redirect to frontend
- [x] Automatic data cleanup on new uploads
- [ ] Multi-user support
- [ ] Chat history persistence
- [ ] Advanced chunking strategies
- [ ] Fine-tuned Turkish embeddings
- [ ] API authentication
- [ ] Streaming responses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Name](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)

---

⭐ Star this repo if you find it useful!
