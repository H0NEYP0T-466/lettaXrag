# LettaXRAG - Conversational AI with RAG & Personality

A full-stack conversational AI system featuring **Isabella**, a sassy AI assistant powered by RAG (Retrieval-Augmented Generation) and comprehensive logging.

> **⚠️ Security Note**: Letta personality engine is disabled by default due to known vulnerabilities. See [SECURITY.md](SECURITY.md) for details. Isabella's personality is maintained through LLM system prompts.

## 🌟 Features

- **🎭 Personality**: Isabella - your sassy, confident AI assistant with attitude
- **📚 RAG System**: FAISS-based document retrieval for knowledge-enhanced responses
- **💬 Real-time Chat**: Beautiful, responsive chat interface
- **📁 Document Upload**: Support for .txt, .md, .pdf, and .docx files
- **🔍 Rich Logging**: Comprehensive colored console logs tracking every step
- **💾 MongoDB Storage**: Persistent conversation history
- **🔒 Security**: Updated dependencies with patched vulnerabilities

## 🏗️ Architecture

### Frontend (React + TypeScript)
- Modern React 19 with TypeScript
- Zustand for state management
- Axios for API communication
- Beautiful gradient UI with animations

### Backend (Python FastAPI)
- FastAPI with async support (v0.109.1+ - patched)
- MongoDB for data persistence
- FAISS-CPU for vector similarity search
- Sentence-transformers for embeddings
- ~~Letta for personality management~~ (disabled - see SECURITY.md)
- LongCat LLM API integration
- Rich library for beautiful console logging

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
LETTA_API_KEY=your_letta_key_here  # Optional
DATA_FOLDER=./data
FAISS_INDEX_PATH=./storage/faiss_index.bin
LOG_LEVEL=DEBUG
```

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
2. Type your question in the input box
3. Press Enter or click the send button
4. Isabella will respond using her personality and knowledge base!

### Upload Documents

1. Click the "📤 Upload Document" button in the header
2. Select a supported file (.txt, .md, .pdf, .docx)
3. The system will automatically re-index the document
4. Isabella can now use this knowledge in her responses!

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

Edit `backend/services/letta_service.py`:

```python
self.persona = """Your custom personality here..."""
```

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
