# 🧠 Agentic AI Fashion Assistant

A local AI-powered fashion recommendation system that combines computer vision, retrieval-augmented generation (RAG), and large language models (LLMs) to generate personalized outfit recommendations with detailed reasoning.

---

## ✅ Key Features

- 👔 **Smart Outfit Recommendations** - Generates personalized outfit suggestions based on occasion
- 🖼️ **Vision Analysis** - Analyzes uploaded clothing images to detect items, colors, patterns, and materials
- 📚 **Knowledge-Based RAG** - Retrieves relevant fashion rules from a curated knowledge base
- 🤖 **Local LLM Integration** - Uses Ollama for privacy-first recommendation generation
- 💬 **Detailed Explanations** - Provides reasoning for outfit choices
- 🔄 **Alternative Suggestions** - Offers alternative outfit options
- ⭐ **Style Scoring** - Rates outfits with a style score (1-10)
- 🖥️ **User-Friendly UI** - Streamlit web interface for easy interaction

---
<img width="935" height="410" alt="image" src="https://github.com/user-attachments/assets/23cba3e8-299a-4854-a024-03514e34d9de" />

<img width="533" height="372" alt="image" src="https://github.com/user-attachments/assets/f12fc2c7-2043-4389-ab0e-4af7f7a353e9" />

<img width="155" height="228" alt="image" src="https://github.com/user-attachments/assets/80c1265b-46a6-4f3e-9924-bdd6757afbe4" />


## 🏗️ System Architecture

### High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (FRONTEND)                │
│                    Streamlit Web Application                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ • Input: Occasion + Optional Image Upload                │   │
│  │ • Display: Recommendations, Reasoning, Alternatives      │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    HTTP POST /recommend
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (BACKEND)                        │
│                      FastAPI Application                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ • Route: POST /recommend                                  │   │
│  │ • Handles: File uploads, Form data, Error handling       │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    FashionOrchestrator.recommend()
                                 │
        ┌────────────┬───────────┴──────────┬─────────────┐
        │            │                      │             │
        ▼            ▼                      ▼             ▼
   ┌─────────┐  ┌──────────┐          ┌─────────┐  ┌──────────┐
   │ VISION  │  │   RAG    │          │   LLM   │  │ORCHESTR. │
   │ MODULE  │  │ RETRIEVER│          │ ENGINE  │  │CONTROL   │
   └─────────┘  └──────────┘          └─────────┘  └──────────┘
        │            │                      │             │
        └────────────┼──────────────────────┼─────────────┘
                     │                      │
                     ▼                      ▼
            ┌──────────────────┐  ┌──────────────────────┐
            │   CHROMA DB      │  │  OLLAMA LOCAL LLM    │
            │ (Vector Store)   │  │ (Mistral/Llama3/etc) │
            └──────────────────┘  └──────────────────────┘

                    ▲                      │
                    │                      │
            ┌───────────────┐              │
            │  rules.txt    │              │
            │(Knowledge Base)           Response JSON
            └───────────────┘              │
                                           ▼
                                   ┌────────────────┐
                                   │  Final Result  │
                                   │  (JSON)        │
                                   └────────────────┘
```

---

## 🧩 Architecture Components

### 1. **Frontend Layer** (`frontend/app.py`)
**Technology:** Streamlit

**Responsibilities:**
- User input collection (occasion, image upload)
- API communication with backend
- Result visualization and display
- Error handling and user feedback

**Flow:**
```
User Input → Form Validation → HTTP Request → Display Results
```

---

### 2. **API Layer** (`backend/main.py`)
**Technology:** FastAPI + Uvicorn

**Endpoints:**
- `POST /recommend` - Main recommendation endpoint
  - Input: `occasion` (string), `image` (optional file)
  - Output: JSON with recommendations, reasoning, alternatives, score

**Responsibilities:**
- Request validation
- File upload handling
- Orchestrator invocation
- Response formatting
- Error handling

---

### 3. **Orchestration Layer** (`backend/orchestrator.py`)
**Technology:** Python (Core business logic)

**Class:** `FashionOrchestrator`

**Pipeline Stages:**

```
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: VISION PROCESSING (Optional)                  │
│ • Checks if image provided                              │
│ • Calls VisionModel.analyze_image()                     │
│ • Extracts: item types, colors, patterns, materials    │
│ • Output: {items: [...]}                                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: RAG RETRIEVAL                                 │
│ • Calls RAGRetriever.retrieve_rules()                   │
│ • Query: User's occasion                                │
│ • Retrieves: Top 5 matching fashion rules               │
│ • Source: ChromaDB vector store                         │
│ • Output: List[str] (relevant fashion rules)            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: CONTEXT ASSEMBLY                              │
│ • Combines all information:                             │
│   - Vision output (detected items)                      │
│   - Occasion (user input)                               │
│   - Retrieved rules (fashion guidance)                  │
│ • Output: context dictionary                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 4: LLM GENERATION                                │
│ • Calls LLMEngine.generate_outfit()                     │
│ • Sends structured prompt to Ollama                     │
│ • Ollama generates detailed recommendation              │
│ • Parses JSON response                                  │
│ • Output: {outfit, reasoning, alternative, style_score}│
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 5: RESPONSE ASSEMBLY                             │
│ • Adds detected items to recommendation                 │
│ • Includes fallback if any stage fails                  │
│ • Returns final JSON response                           │
└─────────────────────────────────────────────────────────┘
```

**Key Methods:**
- `recommend(occasion, image_bytes)` - Main orchestration method
- `_create_fallback_response()` - Fallback when pipeline fails

---

### 4. **Vision Module** (`backend/vision/vision_model.py`)
**Technology:** Ollama LLaVA (multimodal vision model)

**Class:** `VisionModel`

**Responsibilities:**
- Image decoding from bytes
- Image encoding to base64
- Calling LLaVA vision model
- Parsing vision model output
- Extracting clothing metadata

**Detection Output:**
```json
{
  "items": [
    {
      "type": "t-shirt",
      "color": "blue",
      "pattern": "solid",
      "material": "cotton"
    }
  ]
}
```

**Model:** `llava:7b` (Ollama's vision model)

**Process:**
1. Convert image bytes to base64
2. Send to Ollama with vision prompt
3. Parse returned JSON
4. Extract clothing items and attributes

---

### 5. **RAG (Retrieval-Augmented Generation) Module**

#### 5a. **Ingestion** (`backend/rag/ingest.py`)
**Class:** `RAGIngestor`

**Responsibilities:**
- Read fashion rules from `rules.txt`
- Split rules into individual statements
- Generate embeddings using SentenceTransformer
- Store embeddings in ChromaDB

**Process:**
```
rules.txt → Parse → Embed (all-MiniLM-L6-v2) → Store in ChromaDB
```

**Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Database:** ChromaDB (persistent at `backend/rag/chroma_db`)

---

#### 5b. **Retrieval** (`backend/rag/retrieve.py`)
**Class:** `RAGRetriever`

**Responsibilities:**
- Accept user query (occasion)
- Generate query embedding
- Search ChromaDB for similar rules
- Return top-k results

**Process:**
```
Query → Embed → Search ChromaDB → Return Top-5 Rules
```

**Key Method:** `retrieve_rules(query, top_k=5)`

**Uses Same Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`

---

### 6. **LLM Engine** (`backend/llm/llm_engine.py`)
**Technology:** Ollama (local inference)

**Class:** `LLMEngine`

**Responsibilities:**
- Build detailed prompts from context
- Call Ollama API with structured prompts
- Parse JSON responses
- Normalize and validate output
- Provide fallback responses

**Default Model:** `llama3.1`

**Available Models:** Any Ollama-compatible model (mistral, llama3, neural-chat, etc.)

**Prompt Structure:**
```
SYSTEM: You are a fashion expert...
CONTEXT:
- Detected items: [vision output]
- Occasion: [user occasion]
- Fashion rules: [retrieved rules]

TASK: Generate outfit recommendation in JSON format
REQUIRED FORMAT:
{
  "outfit": ["item1", "item2", "item3"],
  "reasoning": "explanation...",
  "alternative": ["alt1", "alt2", "alt3"],
  "style_score": 8.5
}
```

**Output Validation:**
- Ensures JSON format
- Validates required fields
- Provides sensible defaults for missing fields
- Clamps style_score to 1-10 range

---

### 7. **Data Flow: Complete Example**

```
USER INPUT:
  Occasion: "summer beach party"
  Image: photo of blue linen shirt

STEP 1 - VISION:
  LLaVA analyzes image
  → Returns: [{type: "shirt", color: "blue", pattern: "solid", material: "linen"}]

STEP 2 - RAG:
  Query: "summer beach party"
  Embedding + ChromaDB search
  → Returns top-5 rules like:
     1. "Beach wear should prioritize breathable fabrics"
     2. "Light colors are ideal for summer occasions"
     3. "Sunscreen-friendly clothing includes UV protection"
     ... etc

STEP 3 - CONTEXT:
  {
    "vision": {items: [detected shirt]},
    "occasion": "summer beach party",
    "rules": [retrieved fashion rules]
  }

STEP 4 - LLM:
  Ollama generates:
  {
    "outfit": ["blue linen shirt", "white shorts", "sandals"],
    "reasoning": "Light colors keep you cool...",
    "alternative": ["light dress", "beach cover-up"],
    "style_score": 9.2
  }

STEP 5 - RESPONSE:
  {
    "outfit": [...],
    "reasoning": "...",
    "alternative": [...],
    "style_score": 9.2,
    "detected_items": [shirt info]
  }
```

---

## 📂 Detailed Project Structure

```
fashion-ai-assistant/
│
├── README.md                          # Project documentation (this file)
├── requirements.txt                   # Python dependencies
│
├── backend/                           # Backend application
│   ├── __init__.py                    # Package initialization
│   ├── main.py                        # FastAPI application
│   │                                  # ├─ Defines POST /recommend endpoint
│   │                                  # └─ Orchestrates request-response cycle
│   │
│   ├── orchestrator.py                # FashionOrchestrator class
│   │                                  # ├─ Coordinates all pipeline stages
│   │                                  # ├─ Vision → RAG → LLM flow
│   │                                  # └─ Error handling & fallbacks
│   │
│   ├── vision/                        # Vision module
│   │   ├── __init__.py
│   │   ├── vision_model.py            # VisionModel class
│   │   │                              # ├─ Calls Ollama LLaVA
│   │   │                              # └─ Analyzes images for clothing items
│   │   └── testllava.py               # Testing utilities
│   │
│   ├── rag/                           # Retrieval-Augmented Generation module
│   │   ├── __init__.py
│   │   ├── ingest.py                  # RAGIngestor class
│   │   │                              # ├─ Reads rules.txt
│   │   │                              # ├─ Generates embeddings
│   │   │                              # └─ Stores in ChromaDB
│   │   │
│   │   ├── retrieve.py                # RAGRetriever class
│   │   │                              # ├─ Queries user occasion
│   │   │                              # ├─ Searches ChromaDB
│   │   │                              # └─ Returns top-k rules
│   │   │
│   │   ├── rules.txt                  # Fashion rules knowledge base
│   │   │                              # └─ Curated fashion guidance (seed for embeddings)
│   │   │
│   │   └── chroma_db/                 # ChromaDB persistent storage
│   │       └─ [Generated at runtime]  # Contains embeddings & fashion rules
│   │
│   ├── llm/                           # Large Language Model module
│   │   ├── __init__.py
│   │   └── llm_engine.py              # LLMEngine class
│   │                                  # ├─ Builds prompts
│   │                                  # ├─ Calls Ollama API
│   │                                  # └─ Parses JSON responses
│   │
│   └── utils/                         # Utility functions (placeholder)
│       └── __init__.py
│
├── frontend/                          # Frontend application
│   ├── __init__.py
│   └── app.py                         # Streamlit UI
│                                      # ├─ Input form (occasion + image)
│                                      # ├─ API communication
│                                      # └─ Results display
│
├── chroma_db/                         # [Optional] Top-level ChromaDB instance
│   └─ [May be created during setup]
│
└── venv/                              # Python virtual environment (local)
    └─ [Created during setup]
```

---

## 🔄 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend UI** | Streamlit | Web interface for user interaction |
| **Backend API** | FastAPI + Uvicorn | REST API server |
| **Vision Analysis** | Ollama LLaVA | Image understanding |
| **Embeddings** | SentenceTransformers (all-MiniLM-L6-v2) | Text vectorization |
| **Vector DB** | ChromaDB | Persistent vector storage |
| **LLM Inference** | Ollama (Llama3.1/Mistral/etc) | Recommendation generation |
| **HTTP Client** | Python Requests | API communication |
| **File Handling** | Python-Multipart | File upload processing |
| **Image Processing** | OpenCV, Pillow | Image utilities |
| **Environment** | Python 3.8+ | Runtime |

---

## 📊 Data Models

### Vision Output
```json
{
  "items": [
    {
      "type": "shirt|pants|dress|...",
      "color": "blue|red|...",
      "pattern": "solid|striped|...",
      "material": "cotton|silk|..."
    }
  ]
}
```

### RAG Query Response
```json
[
  "Fashion rule 1",
  "Fashion rule 2",
  "Fashion rule 3",
  "Fashion rule 4",
  "Fashion rule 5"
]
```

### LLM Output / API Response
```json
{
  "outfit": ["item1", "item2", "item3"],
  "reasoning": "Explanation of outfit choice",
  "alternative": ["alt_item1", "alt_item2", "alt_item3"],
  "style_score": 8.5,
  "detected_items": [
    {
      "type": "shirt",
      "color": "blue",
      "pattern": "solid",
      "material": "linen"
    }
  ]
}
```

---

## 🔐 System Guarantees

- ✅ **Local Processing** - All data stays on your machine (Ollama runs locally)
- ✅ **Privacy** - No data sent to external APIs
- ✅ **Fault Tolerance** - Fallback recommendations if any stage fails
- ✅ **Modular Design** - Easy to swap components (e.g., different LLM models)
- ✅ **Extensible** - Add new modules without changing core pipeline

---

## 📂 Project Structure

---

## 🛠️ System Requirements

### Hardware Requirements
- **Processor** - Modern CPU (Intel i5+, AMD Ryzen 5+)
- **RAM** - Minimum 8 GB (16 GB recommended for smooth performance)
- **Disk Space** - ~5-10 GB for models and databases
- **GPU** (Optional) - NVIDIA/AMD GPU accelerates inference significantly

### Software Requirements
- **Python** - 3.8 or later (3.10+ recommended)
- **Ollama** - Latest version (https://ollama.ai)
- **Ollama Models**:
  - `llama3.1` (Default LLM, ~7-13B)
  - `mistral` (Lightweight alternative, ~7B)
  - `llava:7b` (Vision model, already specified in code)

---

## 🚀 Complete Setup and Installation Guide

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

## 🧪 Common Troubleshooting

### Issue: Backend Fails to Connect to Ollama

**Symptoms:** `Connection refused` or `HTTPConnectionPool(host='localhost', port=11434)` errors

**Solutions:**
1. Verify Ollama is running:
   ```powershell
   ollama serve
   ```
2. Check the model is installed:
   ```powershell
   ollama list
   ```
3. Verify the URL in code is correct: `http://localhost:11434`
4. Try accessing Ollama directly:
   ```powershell
   curl http://localhost:11434/api/tags
   ```

---

### Issue: Frontend Cannot Reach Backend

**Symptoms:** `Connection refused` at `http://localhost:8000`

**Solutions:**
1. Verify backend is running on correct port:
   ```powershell
   python -m backend.main
   ```
2. Check for port conflicts:
   ```powershell
   netstat -ano | findstr :8000
   ```
3. Ensure firewall allows localhost connection
4. Try accessing backend directly:
   ```powershell
   curl http://localhost:8000/docs
   ```

---

### Issue: ChromaDB/RAG Initialization Fails

**Symptoms:** `ChromaDB connection error` or `Collection not found`

**Solutions:**
1. Ensure `backend/rag/rules.txt` exists and has content
2. Reingest the rules:
   ```powershell
   cd backend
   python -m rag.ingest
   ```
3. Delete old database and reingest:
   ```powershell
   rmdir /s backend\rag\chroma_db
   python -m rag.ingest
   ```

---

### Issue: Image Upload Produces No Detection

**Symptoms:** `detected_items` is null or empty

**Solutions:**
1. Ensure image is a valid clothing photo:
   - Clear and well-lit
   - At least one clothing item visible
   - Supported formats: JPG, JPEG, PNG
2. Verify LLaVA model is installed:
   ```powershell
   ollama pull llava:7b
   ```
3. Check vision model logs in console output
4. Try with a different, clearer image

---

### Issue: Slow Recommendation Generation

**Symptoms:** Takes 30+ seconds per recommendation

**Solutions:**
1. **Hardware:** More RAM or GPU acceleration helps significantly
2. **Model Size:** Try lighter models:
   ```powershell
   ollama pull mistral  # Smaller LLM
   # Then update backend/llm/llm_engine.py: self.model = "mistral"
   ```
3. **Ollama Settings:** Check CPU/GPU allocation
4. **Network:** Local setup should be fast; check network latency

---

### Issue: Out of Memory Errors

**Symptoms:** `CUDA out of memory` or system freezes

**Solutions:**
1. Use smaller models (quantized versions)
2. Reduce batch size if applicable
3. Allocate more RAM to Ollama
4. Close other applications consuming memory
5. Try CPU-only mode instead of GPU

---

## 🧩 Customization & Extension Guide

### Change the LLM Model

Edit `backend/llm/llm_engine.py`:
```python
def __init__(self, model: str = "mistral"):  # Change from "llama3.1"
    self.model = model
```

Available models:
- `mistral` - Smaller, faster (~7B)
- `llama3.1` - Balanced (~7-13B)
- `neural-chat` - Conversational (~7B)
- `openchat` - Chat-optimized (~7B)

Install with:
```powershell
ollama pull mistral
```

---

### Customize Frontend UI

Edit `frontend/app.py`:
- Change title, colors, layout
- Add new input fields
- Modify result display format
- Add more styling with custom CSS

Example:
```python
st.set_page_config(page_title="My Fashion AI", layout="wide")
```

---

### Enhance Fashion Rules

Edit `backend/rag/rules.txt`:
- Add more fashion guidance
- Organize by occasion or season
- Include specific dress codes
- Add style tips

Then reingest:
```powershell
cd backend
python -m rag.ingest
```

---

### Improve Vision Analysis

Modify `backend/vision/vision_model.py`:
- Adjust LLaVA prompt for specific garment types
- Change parsing logic for output
- Add post-processing for better accuracy
- Use a larger vision model if available

---

### Add Custom Metrics

Create new modules in `backend/`:
- Sentiment analyzer for style feedback
- Trend matcher for current fashion
- Personal preference tracker
- Shopping integration

Then integrate into `orchestrator.py`.

---

## 🔌 API Reference

### POST /recommend

**URL:** `http://localhost:8000/recommend`

**Method:** `POST`

**Request Headers:**
```
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `occasion` | string | Yes | Describes the occasion (e.g., "casual", "formal", "summer party") |
| `image` | file | No | Image file of clothing (JPG, PNG, JPEG) |

**Example Request (cURL):**
```bash
curl -X POST \
  -F "occasion=summer beach party" \
  -F "image=@/path/to/image.jpg" \
  http://localhost:8000/recommend
```

**Example Request (Python):**
```python
import requests

with open("clothing.jpg", "rb") as f:
    files = {"image": f}
    data = {"occasion": "summer beach party"}
    response = requests.post("http://localhost:8000/recommend", files=files, data=data)
    print(response.json())
```

**Response (Success - 200):**
```json
{
  "outfit": [
    "linen shirt",
    "white shorts",
    "sandals"
  ],
  "reasoning": "For a summer beach party, lightweight and breathable fabrics are ideal. Light colors help reflect heat and match the casual beachy vibe.",
  "alternative": [
    "light sundress",
    "beach cover-up",
    "flip-flops"
  ],
  "style_score": 8.7,
  "detected_items": [
    {
      "type": "shirt",
      "color": "blue",
      "pattern": "solid",
      "material": "linen"
    }
  ]
}
```

**Response (Error - 500):**
```json
{
  "error": "An error occurred: [error message]"
}
```

---

## 🎨 Frontend UI Workflow

```
1. Open Streamlit App (http://localhost:8501)
   ├─ Display title and description
   └─ Show input form
   
2. User Input
   ├─ Enter occasion (text input)
   ├─ Optionally upload image
   └─ Click "Get Recommendation" button
   
3. Processing (Spinner shown)
   ├─ Prepare form data
   ├─ Send HTTP POST to backend
   └─ Wait for response
   
4. Results Display
   ├─ Show recommended outfit items
   ├─ Display reasoning
   ├─ Show alternative outfit
   ├─ Display style score
   └─ Show detected clothing items (if image uploaded)
```

---

## 📊 Example Workflows

### Workflow 1: Text-Only Recommendation

```
User: "I have a business meeting tomorrow"
→ No image uploaded
→ RAG retrieves business fashion rules
→ LLM generates formal outfit
→ Response: suit, dress shirt, tie, dress shoes
```

### Workflow 2: Image-Based Recommendation

```
User: "I found this shirt, what should I wear with it?" + Upload shirt image
→ Vision analyzes image → Detects blue cotton shirt
→ RAG retrieves styling rules for blue shirts
→ LLM generates complementary outfit
→ Response: blue shirt + navy pants + white sneakers
```

### Workflow 3: Occasion + Image

```
User: "Casual weekend" + Upload image of jeans
→ Vision detects blue jeans
→ RAG retrieves casual weekend rules
→ LLM suggests casual-appropriate combinations
→ Response: jeans + t-shirt + sneakers
```

---

### Enable Debug Logging

Add debug prints in `backend/orchestrator.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

Then run backend to see detailed logs:
```powershell
python -m backend.main
```

---

### Test Individual Components

**Test Vision Module:**
```python
from backend.vision.vision_model import VisionModel
model = VisionModel()
with open("test_image.jpg", "rb") as f:
    result = model.analyze_image(f.read())
    print(result)
```

**Test RAG Retrieval:**
```python
from backend.rag.retrieve import RAGRetriever
retriever = RAGRetriever()
rules = retriever.retrieve_rules("summer party")
print(rules)
```

**Test LLM:**
```python
from backend.llm.llm_engine import LLMEngine
llm = LLMEngine()
context = {
    "vision": None,
    "occasion": "casual",
    "rules": ["Rule 1", "Rule 2"]
}
result = llm.generate_outfit(context)
print(result)
```

---

## 📦 Dependency Management

### Current Dependencies

```
fastapi                    # Web framework
uvicorn                    # ASGI server
streamlit                  # Frontend framework
requests                   # HTTP client
python-multipart           # File upload handling
opencv-python              # Image processing
pillow                     # Image utilities
chromadb                   # Vector database
sentence-transformers      # Embeddings
transformers               # NLP models
colorthief                 # Color detection
```

### Version Compatibility

- **Python:** 3.8, 3.9, 3.10, 3.11
- **FastAPI:** 0.68+
- **Streamlit:** 1.10+
- **ChromaDB:** 0.3+

### Adding New Dependencies

1. Add to `requirements.txt`
2. Run installation:
   ```powershell
   pip install -r requirements.txt
   ```
3. Document purpose in README

---

## 🤝 Contributing

**How to Contribute:**

1. **Fork** the repository
2. **Create** a feature branch:
   ```powershell
   git checkout -b feature/amazing-feature
   ```
3. **Make** your changes
4. **Test** thoroughly:
   - Run vision module tests
   - Test RAG retrieval
   - Test LLM generation
   - Test full pipeline
5. **Commit** with clear messages:
   ```powershell
   git commit -m "Add: [feature description]"
   ```
6. **Push** to your fork:
   ```powershell
   git push origin feature/amazing-feature
   ```
7. **Submit** a pull request

**Code Style:**
- Follow PEP 8
- Add docstrings for functions/classes
- Keep functions focused and small
- Comment complex logic

---

## 📄 License

This project is available under the **MIT License**.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

See LICENSE file for details.

---

## 🎯 Project Roadmap

### Current Features
- ✅ Vision-based clothing detection
- ✅ RAG-based fashion rules
- ✅ LLM-generated recommendations
- ✅ Streamlit web UI
- ✅ FastAPI backend

### Planned Features
- 📋 User preference learning
- 📋 Style history tracking
- 📋 Seasonal recommendations
- 📋 Multi-image outfit assembly
- 📋 Shopping integration
- 📋 Fashion trend analysis
- 📋 Personal style profile
- 📋 Accessibility improvements

---

## 📞 Support & Contact

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Open a new issue with detailed description
3. Include:
   - Steps to reproduce
   - Error messages/logs
   - Your system info (OS, Python version, RAM)
   - Screenshots if applicable

---

## 🔗 Quick Links

- **Ollama:** https://ollama.ai
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Streamlit Docs:** https://docs.streamlit.io
- **ChromaDB Docs:** https://docs.trychroma.com
- **SentenceTransformers:** https://www.sbert.net

---

## 📚 Additional Resources

### Fashion AI Learning
- Understanding RAG systems
- Prompt engineering for LLMs
- Vision model fine-tuning
- Vector database optimization

### Local LLM Setup
- Running Ollama models locally
- GPU acceleration setup
- Model quantization
- Performance optimization

---

## ✨ Key Takeaways

| Aspect | Implementation |
|--------|-----------------|
| **Privacy** | All processing local, no external APIs |
| **Scalability** | Can add more rules, swap models, extend modules |
| **Modularity** | Each component (Vision, RAG, LLM) is independent |
| **Extensibility** | Easy to add new features without breaking core |
| **Robustness** | Fallback mechanisms if any stage fails |
| **User Experience** | Simple UI for end-users, powerful API for integration |

---

**Last Updated:** June 2026  
**Version:** 1.0  
**Status:** Active Development
