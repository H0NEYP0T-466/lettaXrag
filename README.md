# LettaXRAG - Conversational AI with RAG & Personality

<p align="center">
  <img src="https://img.shields.io/github/license/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/forks/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Forks">
  <img src="https://img.shields.io/github/issues/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Issues">
  <img src="https://img.shields.io/github/issues-pr/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Pull Requests">
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Last Commit">
  <img src="https://img.shields.io/github/commit-activity/m/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Commit Activity">
  <img src="https://img.shields.io/github/languages/top/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Top Language">
  <img src="https://img.shields.io/github/languages/count/H0NEYP0T-466/lettaXrag?style=for-the-badge" alt="Languages">
</p>

A full-stack conversational AI system featuring **Isabella**, a sassy AI assistant powered by RAG (Retrieval-Augmented Generation) and comprehensive logging.

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-api-endpoints">API</a> •
  <a href="https://github.com/H0NEYP0T-466/lettaXrag/issues">Issues</a> •
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

> **⚠️ Security Note**: Letta personality engine is disabled by default due to known vulnerabilities. See [SECURITY.md](SECURITY.md) for details. Isabella's personality is maintained through LLM system prompts.

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [System Flow](#-system-flow)
- [Customization](#-customization)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Dependencies](#-dependencies)
- [Troubleshooting](#-troubleshooting)
- [Security Notes](#-security-notes)
- [License](#-license)
- [Contributing](#-contributing)

---

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

## 📋 Prerequisites

- **Node.js** 18+ and npm
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

---

## 🛠 Tech Stack

### Frontend
<p>
  <img src="https://img.shields.io/badge/React-19.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.9.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-7.2.4-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Zustand-5.0.10-000000?style=for-the-badge" alt="Zustand">
</p>

### Backend
<p>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109.1+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MongoDB-Latest-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
</p>

### AI & ML
<p>
  <img src="https://img.shields.io/badge/FAISS-CPU-00ADD8?style=for-the-badge" alt="FAISS">
  <img src="https://img.shields.io/badge/Sentence_Transformers-Latest-FF6F00?style=for-the-badge" alt="Sentence Transformers">
  <img src="https://img.shields.io/badge/OpenAI-Compatible-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
</p>

### Development & Build Tools
<p>
  <img src="https://img.shields.io/badge/ESLint-9.39.1-4B32C3?style=for-the-badge&logo=eslint&logoColor=white" alt="ESLint">
  <img src="https://img.shields.io/badge/Uvicorn-Latest-499848?style=for-the-badge" alt="Uvicorn">
  <img src="https://img.shields.io/badge/Rich-13.7.0+-009485?style=for-the-badge" alt="Rich">
</p>

---

## 📦 Dependencies

### Frontend Dependencies

#### Runtime
![react](https://img.shields.io/npm/v/react?style=for-the-badge&label=react&logo=react&color=61DAFB)
![react-dom](https://img.shields.io/npm/v/react-dom?style=for-the-badge&label=react-dom&logo=react&color=61DAFB)
![axios](https://img.shields.io/npm/v/axios?style=for-the-badge&label=axios&color=5A29E4)
![zustand](https://img.shields.io/npm/v/zustand?style=for-the-badge&label=zustand&color=000000)
![react-markdown](https://img.shields.io/npm/v/react-markdown?style=for-the-badge&label=react-markdown&color=000000)
![react-syntax-highlighter](https://img.shields.io/npm/v/react-syntax-highlighter?style=for-the-badge&label=react-syntax-highlighter&color=000000)
![katex](https://img.shields.io/npm/v/katex?style=for-the-badge&label=katex&color=008080)
![rehype-katex](https://img.shields.io/npm/v/rehype-katex?style=for-the-badge&label=rehype-katex&color=000000)
![remark-gfm](https://img.shields.io/npm/v/remark-gfm?style=for-the-badge&label=remark-gfm&color=000000)
![remark-math](https://img.shields.io/npm/v/remark-math?style=for-the-badge&label=remark-math&color=000000)

#### Development
![typescript](https://img.shields.io/npm/v/typescript?style=for-the-badge&label=typescript&logo=typescript&color=3178C6)
![vite](https://img.shields.io/npm/v/vite?style=for-the-badge&label=vite&logo=vite&color=646CFF)
![eslint](https://img.shields.io/npm/v/eslint?style=for-the-badge&label=eslint&logo=eslint&color=4B32C3)
![typescript-eslint](https://img.shields.io/npm/v/typescript-eslint?style=for-the-badge&label=typescript-eslint&color=3178C6)

### Backend Dependencies

#### Runtime
- **FastAPI** (>=0.109.1) - Modern async web framework
- **Uvicorn** (>=0.24.0) - ASGI server
- **PyMongo** (>=4.6.0) - MongoDB driver
- **Motor** (>=3.3.2) - Async MongoDB driver
- **Pydantic** (>=2.5.0) - Data validation
- **FAISS-CPU** (>=1.7.4) - Vector similarity search
- **Sentence-Transformers** (>=2.2.2) - Text embeddings
- **OpenAI** (>=1.6.1) - LLM API client
- **Letta** (>=0.16.0) - Personality engine (optional)
- **Rich** (>=13.7.0) - Console logging
- **Watchdog** (>=3.0.0) - File system monitoring
- **Python-DOCX** (>=1.1.0) - Word document processing
- **PyPDF2** (>=3.0.1) - PDF processing

#### Development
- **python-dotenv** (>=1.0.0) - Environment variable management
- **python-multipart** (>=0.0.18) - Form data parsing

---

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

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with 💅 by the LettaXRAG Team**
