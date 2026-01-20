# Getting Started Checklist

Use this checklist to ensure you have everything set up correctly for LettaXRAG.

## ☑️ Prerequisites

Before you begin, make sure you have:

- [ ] **Node.js 18+** installed
  ```bash
  node --version  # Should be 18.x or higher
  ```

- [ ] **Python 3.9+** installed
  ```bash
  python3 --version  # Should be 3.9 or higher
  ```

- [ ] **MongoDB** installed and running
  ```bash
  # Test connection
  mongo --eval "db.version()"
  # OR for MongoDB 5+
  mongosh --eval "db.version()"
  ```

- [ ] **LongCat API Key** obtained
  - Visit: https://longcat.chat
  - Sign up / Login
  - Get your API key from dashboard

## ☑️ Installation Steps

### 1. Clone Repository
- [ ] Clone the repository
  ```bash
  git clone https://github.com/H0NEYP0T-466/lettaXrag.git
  cd lettaXrag
  ```

### 2. Backend Setup
- [ ] Navigate to backend folder
  ```bash
  cd backend
  ```

- [ ] Create Python virtual environment
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  # Linux/macOS
  source venv/bin/activate
  
  # Windows
  venv\Scripts\activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```
  ⏱️ This may take 5-10 minutes

- [ ] Create .env file
  ```bash
  cp .env.example .env
  ```

- [ ] Edit .env with your API keys
  ```bash
  nano .env  # or use your preferred editor
  ```
  
  Required fields:
  ```env
  MONGODB_URI=mongodb://localhost:27017/lettaXrag
  LONGCAT_API_KEY=your_actual_api_key_here
  ```

### 3. Frontend Setup
- [ ] Return to root directory
  ```bash
  cd ..  # Back to lettaXrag root
  ```

- [ ] Install Node dependencies
  ```bash
  npm install
  ```
  ⏱️ This may take 2-5 minutes

- [ ] Create frontend .env (optional)
  ```bash
  cp .env.example .env
  ```
  
  Default is fine for local development:
  ```env
  VITE_API_URL=http://localhost:8000
  ```

### 4. Add Documents (Optional)
- [ ] Add your documents to the data folder
  ```bash
  # Add .txt, .md, .pdf, or .docx files
  cp /path/to/your/documents/*.pdf backend/data/
  ```

## ☑️ Running the Application

### Start Backend
- [ ] Open Terminal 1
- [ ] Navigate to backend
  ```bash
  cd backend
  ```
- [ ] Activate virtual environment
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  ```
- [ ] Start the server
  ```bash
  python main.py
  ```

**Expected output:**
```
🚀 Starting LettaXRAG backend...
✅ Connected to MongoDB: mongodb://localhost:27017/lettaXrag
✅ Loading existing embeddings... (or 🔄 Generating embeddings...)
✅ Letta personality engine ready!
ℹ️  Started watching folder: ./data
✅ LettaXRAG backend ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

- [ ] Verify backend is running
  ```bash
  # In another terminal
  curl http://localhost:8000/api/health
  ```

### Start Frontend
- [ ] Open Terminal 2
- [ ] Navigate to root directory
  ```bash
  cd lettaXrag  # if not already there
  ```
- [ ] Start development server
  ```bash
  npm run dev
  ```

**Expected output:**
```
VITE v7.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

- [ ] Open browser to http://localhost:5173

## ☑️ Testing the System

### Basic Tests
- [ ] **UI Loads**: You see Isabella's welcome message
- [ ] **Connection Status**: Shows "Connected" in header
- [ ] **Send Message**: Type "Hello" and press Enter
- [ ] **Get Response**: Isabella responds with personality
- [ ] **Check Logs**: Backend terminal shows colored logs

### RAG Tests
- [ ] **Ask about documents**: "What is RAG?"
- [ ] **See sources**: Click "Show Sources" button
- [ ] **Verify retrieval**: Backend logs show RAG retrieval

### Upload Tests
- [ ] **Click Upload**: Click "📤 Upload Document"
- [ ] **Select file**: Choose a .txt, .md, .pdf, or .docx file
- [ ] **Upload success**: See success message
- [ ] **Check indexing**: Backend logs show re-indexing
- [ ] **Query new doc**: Ask a question about the uploaded document

### Health Check
- [ ] **API Health**: Visit http://localhost:8000/api/health
- [ ] **Response**: Should show all services "healthy"

### Stats Check
- [ ] **API Stats**: Visit http://localhost:8000/api/stats
- [ ] **Response**: Shows message count and document count

## ☑️ Verification Checklist

### Backend Verification
- [ ] Backend starts without errors
- [ ] MongoDB connection successful
- [ ] FAISS index loads/generates
- [ ] Letta initializes (or gracefully skips)
- [ ] File watcher starts
- [ ] Colored logs appear in console
- [ ] Health endpoint returns 200
- [ ] Can access API docs at http://localhost:8000/docs

### Frontend Verification
- [ ] Frontend builds successfully (`npm run build`)
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] UI renders correctly
- [ ] Can send messages
- [ ] Messages persist in UI
- [ ] Upload button works
- [ ] Sources display correctly

### Integration Verification
- [ ] Frontend connects to backend
- [ ] Messages save to MongoDB
- [ ] RAG retrieves documents
- [ ] LLM generates responses
- [ ] Sources are displayed
- [ ] File upload triggers re-indexing

## 🚨 Common Issues

### Issue: MongoDB Connection Failed
**Symptom:** "Failed to connect to MongoDB"

**Solution:**
```bash
# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
# Or run mongod manually
mongod --dbpath /path/to/data
```

### Issue: Port 8000 Already in Use
**Symptom:** "Address already in use"

**Solution:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
# OR change port in backend/main.py
```

### Issue: Frontend Shows "Disconnected"
**Symptom:** Red status indicator

**Solution:**
1. Check backend is running
2. Check backend URL in .env
3. Check browser console for errors

### Issue: No Documents in RAG
**Symptom:** "No documents in index for retrieval"

**Solution:**
1. Add documents to `backend/data/`
2. Restart backend to trigger indexing
3. Or upload via UI

### Issue: Letta Fails to Initialize
**Symptom:** "Error initializing Letta"

**Solution:**
- This is expected if Letta API key not configured
- System will continue without Letta
- Isabella still works but without personality processing

## 📚 Next Steps

Once everything is working:

- [ ] **Customize Isabella**: Edit `backend/services/letta_service.py`
- [ ] **Add More Documents**: Drop files into `backend/data/`
- [ ] **Adjust RAG Settings**: Edit `backend/services/rag_service.py`
- [ ] **Change LLM Settings**: Edit `backend/services/llm_service.py`
- [ ] **Read Documentation**: Check README.md, API.md, ARCHITECTURE.md
- [ ] **Explore API**: Visit http://localhost:8000/docs

## 🎓 Learning Resources

- **README.md** - Setup and usage guide
- **API.md** - API reference with examples
- **TESTING.md** - Comprehensive testing guide
- **ARCHITECTURE.md** - System design details
- **SUMMARY.md** - Project overview

## ✅ Success Criteria

You're ready to go when:
- ✅ Both backend and frontend are running
- ✅ No errors in either terminal
- ✅ UI shows "Connected" status
- ✅ Can send and receive messages
- ✅ RAG sources appear in responses
- ✅ Console logs are colorful and detailed
- ✅ File upload works

## 🎉 You're All Set!

If all checkboxes are checked, you're ready to:
- Chat with Isabella
- Upload documents
- Ask questions
- Get knowledge-enhanced responses
- Enjoy your sassy AI assistant!

**Have fun with LettaXRAG! 💅✨**

---

**Need help?** Open an issue on GitHub or check the documentation files.
