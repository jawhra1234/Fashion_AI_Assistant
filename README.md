# 🧠 Agentic AI Fashion Assistant

This repository is a local AI-powered fashion recommendation system. It combines optional image analysis, retrieval-augmented generation (RAG), and a local LLM service to recommend outfits and explain why they work.

---

## ✅ What This Project Does

- Accepts an occasion description from the user
- Optionally accepts a clothing image upload
- Uses a vision module to identify clothing type and color from the image
- Uses a RAG module to retrieve fashion rules from a knowledge base
- Uses an LLM via Ollama to create an outfit recommendation
- Returns structured output with:
  - recommended outfit
  - explanation/reasoning
  - alternative outfit
  - style score

---

## 🧩 Architecture

The app is organized into three main parts:

1. **Frontend** (`frontend/app.py`)
   - Streamlit user interface
   - Accepts occasion and image input
   - Sends requests to the backend
   - Displays the recommendation result

2. **Backend API** (`backend/main.py`)
   - FastAPI server with `POST /recommend`
   - Handles form and file upload processing
   - Uses the orchestrator to run the recommendation pipeline

3. **Recommendation pipeline** (`backend/orchestrator.py`)
   - Coordinates vision processing, RAG retrieval, and LLM generation
   - Builds the input context for the LLM
   - Handles fallback responses and error cases

---

## 📂 Project Structure

```
fashion-ai-assistant/
├── backend/
│   ├── main.py              # FastAPI application and endpoint
│   ├── orchestrator.py      # Pipeline orchestration logic
│   ├── llm/
│   │   └── llm_engine.py    # Ollama prompt generation and parsing
│   ├── rag/
│   │   ├── ingest.py        # Fashion rule ingestion into ChromaDB
│   │   ├── retrieve.py      # Rule retrieval using embeddings
│   │   └── rules.txt        # Fashion rules knowledge base
│   ├── vision/
│   │   └── vision_model.py  # Image analysis and color detection
│   └── utils/               # Utility helper package (empty placeholder)
├── frontend/
│   └── app.py               # Streamlit web interface
├── requirements.txt         # Required Python packages
└── README.md                # Project documentation
```

---

## 🛠️ Requirements

- Python 3.8 or later
- Ollama installed locally
- A downloaded Ollama model such as `mistral` or `llama3`
- Recommended: 8+ GB RAM for local model usage

---

## 🚀 Setup and Run Instructions

### 1. Create and Activate Virtual Environment

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If using `cmd.exe`:

```cmd
venv\Scripts\activate.bat
```

---

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 3. Install and Start Ollama

Install Ollama from https://ollama.ai and start the service.

Pull a model such as:

```powershell
ollama pull mistral
# or
ollama pull llama3
```

To run Ollama:

```powershell
ollama serve
```

> The backend expects Ollama to be reachable at `http://localhost:11434`.

---

### 4. Ingest Fashion Rules

The knowledge base is stored in `backend/rag/rules.txt` and must be loaded into ChromaDB.

```powershell
cd backend
python -m rag.ingest
```

This creates the persistent vector store under `backend/rag/chroma_db`.

---

### 5. Start the Backend API

From the project root:

```powershell
python -m backend.main
```

The backend listens on:

- `http://localhost:8000`

---

### 6. Start the Frontend UI

In a new terminal from the project root:

```powershell
streamlit run frontend/app.py
```

Then open the Streamlit interface in your browser at:

- `http://localhost:8501`

---

## 🎯 How to Use the App

1. Open the Streamlit UI
2. Enter the occasion or event
3. Optionally upload a photo of a clothing item
4. Click `Get Recommendation`
5. Review:
   - recommended outfit items
   - reasoning
   - alternative option
   - style score

---

## 🔍 What Each Module Does

### `backend/vision/vision_model.py`
- Reads uploaded image bytes
- Uses OpenCV to decode the image
- Crops image edges to reduce background noise
- Detects dominant color with KMeans
- Converts RGB values into a named color
- Guesses garment type from aspect ratio
- Returns structured item metadata

### `backend/rag/ingest.py`
- Reads `rules.txt`
- Splits content into individual rules
- Computes embeddings using `SentenceTransformer('all-MiniLM-L6-v2')`
- Stores text and embeddings in ChromaDB

### `backend/rag/retrieve.py`
- Embeds the user query (`occasion`)
- Queries ChromaDB for the top matching rules
- Returns the most relevant rules to the orchestrator

### `backend/llm/llm_engine.py`
- Builds a prompt using:
  - detected vision items
  - occasion text
  - retrieved fashion rules
- Sends the prompt to Ollama
- Parses the response into JSON
- Normalizes output fields and provides fallback defaults

### `backend/orchestrator.py`
- Coordinates the full recommendation flow
- Calls the vision module if an image is provided
- Calls RAG retrieval for fashion guidance
- Calls the LLM to generate final output
- Returns a response that includes `detected_items`

### `backend/main.py`
- Defines the `/recommend` API route
- Accepts `occasion` and optional image upload
- Returns structured JSON from the orchestrator

### `frontend/app.py`
- Streamlit application UI
- Sends requests to backend with form data and file uploads
- Displays the recommendation result clearly

---

## ⚠️ Important Notes

- The vision logic is simple and heuristic-based, not a full object detector.
- The system relies on Ollama being available locally.
- The RAG module only uses the rules stored in `backend/rag/rules.txt`.
- If any stage fails, the system returns fallback recommendations.

---

## 🧪 Common Troubleshooting

### Backend fails to connect to Ollama
- Confirm Ollama is running: `ollama serve`
- Confirm the model is installed: `ollama list`
- Confirm the URL is `http://localhost:11434`

### Frontend cannot reach backend
- Confirm backend is running on port `8000`
- Confirm there is no port conflict or firewall rule

### Rule retrieval not matching well
- Edit `backend/rag/rules.txt`
- Re-run `python -m rag.ingest`

### Image upload produces no detection
- Upload a clear clothing image
- Supported formats: `jpg`, `jpeg`, `png`

---

## 🧩 Customization Tips

- To change the LLM model, edit `backend/llm/llm_engine.py` and update `self.model`.
- To change the appearance or inputs of the UI, edit `frontend/app.py`.
- To add more fashion guidance, update `backend/rag/rules.txt` and re-ingest.

---

## 📦 Dependencies

- `fastapi`
- `uvicorn`
- `streamlit`
- `requests`
- `python-multipart`
- `opencv-python`
- `pillow`
- `chromadb`
- `sentence-transformers`
- `transformers`
- `colorthief`

---

## 🤝 Contributing

- Fork the repository
- Create a feature branch
- Make and test your changes
- Submit a pull request

---

## 📄 License

This project is available under the MIT License.
