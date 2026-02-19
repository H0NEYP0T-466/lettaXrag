# LettaXRAG - Conversational AI with RAG & Personality

<p align="center">
  <!-- Repository Stats -->
  <img src="https://img.shields.io/github/license/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="GitHub License">
  <img src="https://img.shields.io/github/stars/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="GitHub Forks">
  <img src="https://img.shields.io/github/issues/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="GitHub Issues">
  <img src="https://img.shields.io/github/issues-pr/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="GitHub Pull Requests">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=for-the-badge" alt="Contributions Welcome">
  <br>
  <!-- Repository Activity -->
  <img src="https://img.shields.io/github/last-commit/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Last Commit">
  <img src="https://img.shields.io/github/commit-activity/m/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Commit Activity">
  <img src="https://img.shields.io/github/repo-size/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Repo Size">
  <img src="https://img.shields.io/github/languages/code-size/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Code Size">
  <br>
  <!-- Language Stats -->
  <img src="https://img.shields.io/github/languages/top/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Top Language">
  <img src="https://img.shields.io/github/languages/count/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Languages Count">
  <br>
  <!-- Community & Documentation -->
  <img src="https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=for-the-badge" alt="Documentation">
  <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg?style=for-the-badge" alt="Open Source Love">
</p>

A full-stack conversational AI system featuring **Isabella**, a sassy AI assistant powered by RAG (Retrieval-Augmented Generation) and comprehensive logging.

> **⚠️ Security Note**: Letta personality engine is disabled by default due to known vulnerabilities. See [SECURITY.md](SECURITY.md) for details. Isabella's personality is maintained through LLM system prompts.

## 🌟 Features

- **🎭 Personality**: Isabella - your sassy, confident AI assistant with attitude
- **📚 RAG System**: FAISS-based document retrieval for knowledge-enhanced responses
- **💬 Real-time Chat**: Terminal-style chat interface with monospace fonts
- **🎨 Rich Rendering**: Full support for Markdown, LaTeX, code syntax highlighting, and tables
- **📁 Document Upload**: Support for .txt, .md, .pdf, and .docx files (backend API)
- **🔍 Rich Logging**: Comprehensive colored console logs tracking every step
- **💾 MongoDB Storage**: Persistent conversation history
- **🔒 Security**: Updated dependencies with patched vulnerabilities
- **📖 Letta Integration**: Optional personality engine (see [LETTA_INFO.md](LETTA_INFO.md))

> **ℹ️ Learn about Letta**: For detailed information about Letta personality engine, how it works, and implementation details, see [LETTA_INFO.md](LETTA_INFO.md)

## 🏗️ Architecture

### Backend (Python FastAPI)
- FastAPI with async support (v0.109.1+ - patched)
- MongoDB for data persistence
- FAISS-CPU for vector similarity search
- Sentence-transformers for embeddings
- Letta for personality management (optional - see [LETTA_INFO.md](LETTA_INFO.md))
- LongCat LLM API integration
- Rich library for beautiful console logging

### Frontend (React + TypeScript)
- Modern React 19 with TypeScript
- Zustand for state management
- Axios for API communication
- Terminal-style UI with monospace fonts
- React-Markdown for Markdown rendering
- KaTeX for LaTeX math rendering
- React-Syntax-Highlighter for code blocks
- Full table rendering support

## 🛠️ Tech Stack & Dependencies

### Backend Stack
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109.1%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MongoDB-Latest-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Motor-Async-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="Motor">
  <br>
  <img src="https://img.shields.io/badge/FAISS-CPU-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="FAISS">
  <img src="https://img.shields.io/badge/Sentence_Transformers-Latest-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white" alt="Sentence Transformers">
  <img src="https://img.shields.io/badge/PyPDF2-Latest-FF2D20?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PyPDF2">
  <img src="https://img.shields.io/badge/Python_Docx-Latest-2B579A?style=for-the-badge&logo=microsoftword&logoColor=white" alt="Python-docx">
  <br>
  <img src="https://img.shields.io/badge/Rich-Console-FF69B4?style=for-the-badge&logo=python&logoColor=white" alt="Rich">
  <img src="https://img.shields.io/badge/Watchdog-Latest-FFA500?style=for-the-badge&logo=python&logoColor=white" alt="Watchdog">
  <img src="https://img.shields.io/badge/Letta-0.16.0-8A2BE2?style=for-the-badge" alt="Letta">
  <img src="https://img.shields.io/badge/LongCat_LLM-API-000000?style=for-the-badge" alt="LongCat LLM">
</p>

### Frontend Stack
<p align="center">
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-Latest-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-Latest-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Node.js-20%2B-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
  <br>
  <img src="https://img.shields.io/badge/Zustand-State-000000?style=for-the-badge&logo=react&logoColor=white" alt="Zustand">
  <img src="https://img.shields.io/badge/Axios-HTTP-5A29E4?style=for-the-badge&logo=axios&logoColor=white" alt="Axios">
  <img src="https://img.shields.io/badge/React_Markdown-Latest-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="React Markdown">
  <img src="https://img.shields.io/badge/KaTeX-Math-228BE6?style=for-the-badge" alt="KaTeX">
  <br>
  <img src="https://img.shields.io/badge/Rehype-Plugins-663399?style=for-the-badge" alt="Rehype">
  <img src="https://img.shields.io/badge/Remark-Plugins-663399?style=for-the-badge" alt="Remark">
  <img src="https://img.shields.io/badge/React_Syntax_Highlighter-Latest-F7DF1E?style=for-the-badge" alt="Syntax Highlighter">
</p>

### Dependencies
**Backend** – Full list with exact versions & security patches in [`backend/requirements.txt`](backend/requirements.txt)  
**Frontend** – Full list with exact versions in [`package.json`](package.json)  

> All dependencies are kept up-to-date with patched vulnerabilities (see [SECURITY.md](SECURITY.md)).

## 📋 Prerequisites

- **Node.js** 20+ and npm
- **Python** 3.9+
- **MongoDB** (local or remote)
- **LongCat API Key** ([Get one here](https://longcat.chat))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/H0NEYP0T-466/lettaXrag.git
cd lettaXrag
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

**Required Environment Variables (.env):**
```env
MONGODB_URI=mongodb://localhost:27017/lettaXrag
LONGCAT_API_KEY=your_actual_api_key_here

# Letta - Local Server (Recommended)
LETTA_BASE_URL=http://localhost:8283
# No LETTA_API_KEY needed for local server

# Letta - Cloud Server (Alternative)
# LETTA_BASE_URL=https://api.letta.com
# LETTA_API_KEY=your_letta_cloud_api_key_here

# Optional
DATA_FOLDER=./data
FAISS_INDEX_PATH=./storage/faiss_index.bin
LOG_LEVEL=DEBUG
```

> **📖 Letta Local Server Setup:** If you want to use Letta personality engine with a local server,
> see [backend/letta.txt](backend/letta.txt) for detailed setup instructions including PostgreSQL
> configuration and troubleshooting.

### 3. Frontend Setup

```bash
# From root directory
npm install

# Create .env file
cp .env.example .env

# Edit if needed (default: http://localhost:8000)
```

### 4. Add Documents (Optional)

Add your knowledge base documents to the `backend/data` folder:

```bash
cd backend/data
# Add your .txt, .md, .pdf, or .docx files here
```

The system will automatically index them on startup!

### 5. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

The backend will start on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🎯 Usage

### Chat with Isabella

1. Open your browser to `http://localhost:5173`
2. Type your question in the terminal-style input box
3. Press Enter or click [send]
4. Isabella will respond using her personality and knowledge base!

### Terminal-Style Interface

The chat interface features:
- **Black background** with green and cyan text (terminal aesthetic)
- **Monospace font** (Courier New) throughout
- **Minimal design** - no gradients, just clean text
- **Rich content rendering**:
  - Markdown formatting (headers, lists, bold, italic, links)
  - LaTeX math equations (inline: `$...$` and display: `$$...$$`)
  - Code blocks with syntax highlighting
  - Tables with proper formatting
  - Blockquotes and other Markdown features

### Upload Documents

Documents can be uploaded via the API endpoint:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/document.pdf"
```

The system will automatically re-index and Isabella can use this knowledge!

### View Sources

When Isabella uses documents to answer your question:
- Click "📚 Show Sources" on her message
- See which documents she referenced

## 🔌 API Endpoints

### POST `/api/chat`
Send a message to Isabella

**Request:**
```json
{
  "message": "What is RAG?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "RAG stands for...",
  "rag_sources": ["document1.pdf", "notes.md"],
  "timestamp": "2026-01-20T12:00:00"
}
```

### GET `/api/health`
Check system health status

### POST `/api/upload`
Upload a new document for indexing

### GET `/api/stats`
Get system statistics (message count, indexed documents)

## 📊 System Flow

1. User sends message → Frontend
2. Frontend POST to `/api/chat` → Backend
3. Backend logs user prompt with Rich
4. **Letta** processes message (adds personality)
5. **RAG** retrieves relevant context from FAISS
6. Constructs final prompt with context
7. Sends to **LongCat LLM** API
8. Logs LLM response
9. Saves to **MongoDB**
10. Returns to frontend
11. Frontend displays Isabella's response

## 🎨 Customization

### Change Isabella's Personality

For Letta-based personality, edit `backend/services/letta_service.py`:

```python
self.persona = """Your custom personality here..."""
```

For LLM-based personality (when Letta is disabled), edit `backend/services/llm_service.py`:

```python
system_prompt = """Your custom personality..."""
```

See [LETTA_INFO.md](LETTA_INFO.md) for detailed information about personality management.

### Adjust RAG Settings

Edit `backend/services/rag_service.py`:

```python
def retrieve_context(self, query: str, k: int = 5):  # Change k value
    # Adjust chunk_size and overlap in _chunk_text()
```

### Modify LLM Settings

Edit `backend/services/llm_service.py`:

```python
temperature=0.7,  # Adjust creativity (0.0-1.0)
max_tokens=1000,  # Adjust response length
```

## 📁 Project Structure

```
lettaXrag/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── db_service.py      # MongoDB operations
│   │   ├── rag_service.py     # FAISS RAG system
│   │   ├── letta_service.py   # Personality engine
│   │   └── llm_service.py     # LongCat integration
│   ├── routes/
│   │   └── chat.py            # API endpoints
│   ├── utils/
│   │   ├── logger.py          # Rich logging
│   │   └── file_watcher.py    # Data folder monitor
│   ├── data/                  # Your documents
│   └── storage/               # FAISS index storage
├── src/
│   ├── components/            # React components
│   ├── services/              # API client
│   ├── hooks/                 # Custom React hooks
│   ├── store/                 # Zustand store
│   └── types/                 # TypeScript types
└── package.json
```

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Make sure MongoDB is running
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
```

### FAISS Index Issues
```bash
# Delete and rebuild index
rm backend/storage/*
# Restart backend - it will rebuild automatically
```

### Letta Initialization Fails
The system will continue without Letta if initialization fails. Isabella will still work but without personality processing.

**Common causes:**
- Letta server not running (if using local server)
- Wrong LETTA_BASE_URL configuration
- PostgreSQL not running (if Letta is configured to use it)

**Solutions:**
- See [backend/letta.txt](backend/letta.txt) for comprehensive Letta setup guide
- Check your `.env` file has: `LETTA_BASE_URL=http://localhost:8283`
- Make sure Letta server is running: `letta server`
- Or disable Letta by commenting out LETTA_BASE_URL in `.env`

### Port Already in Use
```bash
# Change backend port in main.py
uvicorn.run("main:app", host="0.0.0.0", port=8001)

# Update frontend .env
VITE_API_URL=http://localhost:8001
```

## 🔒 Security Notes

⚠️ **Important**: Please review [SECURITY.md](SECURITY.md) for comprehensive security information.

### Quick Security Checklist

- ✅ **Dependencies Updated**: All known vulnerabilities patched
- ⚠️ **Letta Disabled**: Library has unpatched vulnerabilities (see SECURITY.md)
- 🔒 **Environment Variables**: Never commit your `.env` file
- 🔑 **API Keys**: Keep your API keys secure and rotate regularly
- 🌐 **CORS**: Use environment-specific CORS settings in production
- 📁 **File Uploads**: Implement size limits and validation in production
- 🔐 **Authentication**: Add user authentication before production deployment
- 🛡️ **Rate Limiting**: Implement rate limiting for production use

**For Production Deployment**: See the production security checklist in [SECURITY.md](SECURITY.md)

## 📝 License

MIT License - feel free to use this project as you wish!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with 💅 by the LettaXRAG Team**
