# Testing Guide for LettaXRAG

This guide will help you test the LettaXRAG system components.

## Prerequisites

Before testing, ensure you have:
- MongoDB running locally or remotely
- LongCat API key ([Get one here](https://longcat.chat))
- Python 3.9+ and Node.js 18+

## Quick Test Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (IMPORTANT!)
cp .env.example .env
```

Edit `.env` and add your actual API keys:
```env
MONGODB_URI=mongodb://localhost:27017/lettaXrag
LONGCAT_API_KEY=your_actual_longcat_api_key_here
LETTA_API_KEY=optional_letta_key
DATA_FOLDER=./data
FAISS_INDEX_PATH=./storage/faiss_index.bin
LOG_LEVEL=DEBUG
```

### 2. Frontend Setup

```bash
# From root directory
npm install

# Create .env (optional, uses default)
cp .env.example .env
```

## Testing the System

### Test 1: Backend Health Check

Start the backend:
```bash
cd backend
source venv/bin/activate
python main.py
```

Expected output:
```
🚀 Starting LettaXRAG backend...
✅ Connected to MongoDB: mongodb://localhost:27017/lettaXrag
✅ Loading existing embeddings... (or 🔄 Generating embeddings...)
✅ Embeddings ready! Indexed X chunks from Y files
ℹ️  Initializing Letta personality engine...
✅ Letta personality engine ready!
ℹ️  Started watching folder: ./data
✅ LettaXRAG backend ready!
```

Test the health endpoint:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "mongodb": "connected",
  "faiss": "ready",
  "timestamp": "2026-01-20T12:00:00"
}
```

### Test 2: Frontend UI

In a new terminal:
```bash
npm run dev
```

Open browser to http://localhost:5173

Expected:
- See Isabella's welcome message
- Beautiful gradient UI
- Input box at bottom
- Status indicator showing "Connected"

### Test 3: Chat Interaction

In the UI:
1. Type: "What is RAG?"
2. Press Enter

Expected backend logs:
```
📥 USER PROMPT [HH:MM:SS] What is RAG?
🎭 LETTA PROCESSING [HH:MM:SS] <processed message>
📚 RAG SIMILARITY RESULTS [HH:MM:SS]
  1. RAG stands for Retrieval-Augmented Generation...
  2. How RAG Works...
  3. Benefits of RAG...
🚀 FINAL PROMPT TO LLM [HH:MM:SS]
<prompt with RAG context>
🤖 LLM RESPONSE [HH:MM:SS] <Isabella's response>
✅ OUTGOING RESPONSE [HH:MM:SS] <response preview>
✅ Message saved with ID: <mongodb_id>
```

Expected frontend:
- Isabella responds with personality
- "📚 Show Sources" button appears
- Click to see document sources

### Test 4: File Upload

1. Click "📤 Upload Document" button
2. Select a .txt, .md, .pdf, or .docx file
3. Wait for upload

Expected:
- Success message: "✅ filename uploaded and indexed successfully!"
- Backend logs show re-indexing
- New document is now searchable

### Test 5: RAG Context Retrieval

Ask Isabella: "Tell me about yourself"

Expected:
- Response includes information from "about_isabella.md"
- Shows source: "about_isabella.md"
- Backend logs show RAG retrieval from the correct document

### Test 6: Stats Endpoint

```bash
curl http://localhost:8000/api/stats
```

Expected response:
```json
{
  "message_count": 3,
  "indexed_documents": 2,
  "timestamp": "2026-01-20T12:00:00"
}
```

## Common Issues and Solutions

### Issue: MongoDB Connection Failed
**Solution:**
```bash
# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
```

### Issue: Letta Initialization Fails
**Expected:** The system will continue without Letta. Isabella still works but without personality processing.

### Issue: FAISS Index Error
**Solution:**
```bash
# Delete existing index and rebuild
rm backend/storage/*
# Restart backend - it will rebuild automatically
```

### Issue: Frontend shows "Disconnected"
**Solution:**
- Check backend is running on port 8000
- Check VITE_API_URL in frontend .env
- Check browser console for CORS errors

### Issue: "No documents in index for retrieval"
**Expected:** This is normal if no documents are in the data folder. Add documents to `backend/data/`.

## Manual Testing Checklist

- [ ] Backend starts without errors
- [ ] MongoDB connection successful
- [ ] FAISS index initializes/loads
- [ ] Letta initializes (or gracefully skips)
- [ ] File watcher starts
- [ ] Health endpoint returns "healthy"
- [ ] Frontend loads successfully
- [ ] Connection status shows "Connected"
- [ ] Can send a chat message
- [ ] Isabella responds with personality
- [ ] RAG sources are displayed
- [ ] Can upload a document
- [ ] Document is indexed automatically
- [ ] New document is searchable
- [ ] Stats endpoint returns correct counts
- [ ] Console logs are colorful and informative
- [ ] Message is saved to MongoDB

## Performance Testing

### Load Test (Optional)

```bash
# Install hey (HTTP load testing tool)
# Debian/Ubuntu: apt-get install hey
# macOS: brew install hey

# Test chat endpoint with 10 requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is RAG?"}' &
done
wait
```

Expected:
- All requests complete successfully
- Backend logs show all requests
- Response times reasonable (<2s per request)

## Debugging Tips

1. **Check logs:** Backend logs every step with colored output
2. **MongoDB:** Use MongoDB Compass to inspect the `messages` collection
3. **FAISS index:** Check `backend/storage/` for index files
4. **Browser DevTools:** Check Network tab for API calls
5. **Python errors:** Check full stack trace in terminal

## Success Criteria

The system is working correctly if:
- ✅ Backend starts and shows all services ready
- ✅ Frontend connects and shows "Connected" status
- ✅ Chat messages receive responses
- ✅ RAG retrieval works (sources shown)
- ✅ File upload and indexing works
- ✅ Messages saved to MongoDB
- ✅ Rich colored logs appear in console
- ✅ No unhandled exceptions or errors

## Next Steps

After successful testing:
1. Add more documents to the knowledge base
2. Customize Isabella's personality
3. Adjust RAG parameters (chunk size, top-k)
4. Configure production environment
5. Set up proper CORS for production
6. Add authentication if needed

---

Happy Testing! 🚀
