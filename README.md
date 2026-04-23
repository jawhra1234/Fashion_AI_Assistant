# 🧠 Agentic AI Fashion Assistant

A full-stack AI application that provides personalized fashion recommendations using computer vision, retrieval-augmented generation (RAG), and large language models (LLMs).

## 🎯 Features

- **Computer Vision**: Extract clothing information from uploaded images
- **Fashion Knowledge Base**: Retrieve relevant fashion rules using RAG
- **AI Recommendations**: Generate outfit suggestions with reasoning
- **Web Interface**: Clean Streamlit UI for easy interaction
- **Local Execution**: Runs entirely on your machine with free/open-source tools

## 🏗️ Architecture

The system follows a modular pipeline:

```
Input → Vision Module → RAG Retrieval → LLM Reasoning → Output
```

- **Vision Module**: Uses CLIP model to classify clothing items and extract colors
- **RAG Module**: Stores fashion rules in ChromaDB vector database for semantic search
- **LLM Module**: Uses Ollama with Mistral/Llama models for intelligent recommendations
- **Orchestrator**: Coordinates the entire pipeline
- **API**: FastAPI backend serving the recommendations
- **Frontend**: Streamlit web interface

## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running locally
- 8-16GB RAM recommended

## 🚀 Setup Instructions

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

Pull the required model:
```bash
ollama pull mistral
# or
ollama pull llama3
```

### 2. Clone and Setup Project

```bash
# Navigate to project directory
cd fashion-ai-assistant

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Ingest Fashion Rules

```bash
# Navigate to backend directory
cd backend

# Ingest fashion rules into vector database
python -m rag.ingest
```

### 4. Start Backend

```bash
# From project root
python -m backend.main
```

If you prefer to run from the backend folder:

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Start Frontend

Open a new terminal and run:

```bash
# From project root
streamlit run frontend/app.py
```

The web interface will open at `http://localhost:8501`

## 🎮 Usage

1. Open the Streamlit web interface
2. Enter an occasion (e.g., "casual Friday", "formal dinner")
3. Optionally upload an image of clothing
4. Click "Get Recommendation"
5. View your personalized outfit suggestion with reasoning

## 📁 Project Structure

```
fashion-ai-assistant/
│
├── backend/
│   ├── main.py              # FastAPI application
│   ├── orchestrator.py      # Pipeline orchestration
│   ├── vision/
│   │   └── vision_model.py  # CLIP-based clothing analysis
│   ├── rag/
│   │   ├── ingest.py        # Knowledge base ingestion
│   │   ├── retrieve.py      # Rule retrieval
│   │   └── rules.txt        # Fashion rules database
│   ├── llm/
│   │   └── llm_engine.py    # Ollama LLM integration
│   └── utils/               # Utility functions
│
├── frontend/
│   └── app.py               # Streamlit web interface
│
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Configuration

### Changing LLM Model

Edit `backend/llm/llm_engine.py`:

```python
self.model = "llama3"  # or "mistral"
```

### Updating Fashion Rules

1. Edit `backend/rag/rules.txt`
2. Re-run ingestion:
```bash
cd backend
python -m rag.ingest
```

## 🛠️ Troubleshooting

### Backend Connection Issues
- Ensure backend is running on port 8000
- Check for firewall blocking local connections

### Ollama Not Responding
- Verify Ollama is installed and running: `ollama list`
- Check model is pulled: `ollama pull mistral`
- Restart Ollama service

### Vision Module Errors
- Ensure image is in supported format (JPG, PNG)
- Check transformers library installation

### RAG Database Issues
- Delete `backend/rag/chroma_db` folder and re-run ingestion
- Ensure sentence-transformers is installed

## 📦 Dependencies

- **fastapi**: Web API framework
- **uvicorn**: ASGI server
- **transformers**: HuggingFace models (CLIP)
- **sentence-transformers**: Text embeddings
- **chromadb**: Vector database
- **streamlit**: Web interface
- **pillow**: Image processing
- **opencv-python**: Computer vision
- **colorthief**: Color extraction
- **requests**: HTTP client
- **python-multipart**: Form and file uploads for FastAPI

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for CLIP model
- Ollama for local LLM serving
- HuggingFace for transformers library
- ChromaDB for vector storage