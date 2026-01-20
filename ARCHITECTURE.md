# LettaXRAG Architecture

## System Overview

LettaXRAG is a full-stack conversational AI system that combines personality management, retrieval-augmented generation (RAG), and modern web technologies to create an engaging chat experience with Isabella, a sassy AI assistant.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │         React + TypeScript + Vite                   │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │ ChatInterface│  │ MessageBubble│  │ InputBox │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │ FileUpload   │  │  Zustand     │               │    │
│  │  │              │  │  (State)     │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                    Axios HTTP                               │
│                          ▼                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                   REST API (JSON)
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Routes                             │    │
│  │  POST /api/chat  │ GET /api/health                 │    │
│  │  POST /api/upload│ GET /api/stats                  │    │
│  └─────────────┬──────────────────────────────────────┘    │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────┐    │
│  │          Service Layer                              │    │
│  │  ┌────────────┐  ┌────────────┐  ┌─────────────┐  │    │
│  │  │   Letta    │  │    RAG     │  │     LLM     │  │    │
│  │  │ Personality│  │  Service   │  │  (LongCat)  │  │    │
│  │  └────────────┘  └────────────┘  └─────────────┘  │    │
│  │  ┌────────────┐  ┌────────────┐                   │    │
│  │  │  Database  │  │File Watcher│                   │    │
│  │  │  Service   │  │            │                   │    │
│  │  └────────────┘  └────────────┘                   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
              │                │                │
              │                │                │
              ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   MongoDB    │  │    FAISS     │  │  LongCat API │
    │   Database   │  │ Vector Store │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
```

## Data Flow

### Chat Request Flow

```
User Types Message
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Frontend: Capture input & call API                   │
│    - User message from InputBox                         │
│    - Add to local state (Zustand)                       │
│    - POST to /api/chat                                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Backend: Receive request                             │
│    - Log user prompt (Rich console)                     │
│    - Extract message and session_id                     │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Letta: Process personality                           │
│    - Send to Letta agent                                │
│    - Apply Isabella's personality traits                │
│    - Maintain conversation context                      │
│    - Log processed prompt                               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. RAG: Retrieve context                                │
│    - Encode query with sentence-transformer             │
│    - Search FAISS index (top-k similarity)              │
│    - Retrieve relevant document chunks                  │
│    - Log RAG results                                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 5. LLM: Generate response                               │
│    - Construct prompt with RAG context                  │
│    - Log final prompt                                   │
│    - Call LongCat API                                   │
│    - Receive Isabella's response                        │
│    - Log LLM response                                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Database: Save conversation                          │
│    - Create message document                            │
│    - Save to MongoDB                                    │
│    - Log save confirmation                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 7. Backend: Return response                             │
│    - Format ChatResponse                                │
│    - Include RAG sources                                │
│    - Log outgoing response                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 8. Frontend: Display response                           │
│    - Add Isabella's message to state                    │
│    - Render MessageBubble                               │
│    - Show RAG sources (collapsible)                     │
│    - Stop typing indicator                              │
└─────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Frontend Components

#### ChatInterface
- Main container component
- Manages layout and structure
- Handles connection status
- Coordinates child components

#### MessageBubble
- Displays individual messages
- Shows sender (user/Isabella)
- Displays timestamp
- Shows/hides RAG sources

#### InputBox
- Text input with multi-line support
- Send button
- Enter key handling (Shift+Enter for newline)
- Disabled state during processing

#### FileUpload
- File input trigger
- Handles file upload to API
- Shows upload status
- Accepts .txt, .md, .pdf, .docx

### Frontend Services

#### api.ts
- Axios client configuration
- API endpoint wrappers
- Error handling
- Type-safe requests/responses

#### chatStore.ts (Zustand)
- Message history
- Session ID management
- Typing indicator state
- Theme state
- Connection status
- Persistent storage

### Backend Services

#### RAG Service
**Responsibilities:**
- Load documents from data folder
- Generate embeddings
- Manage FAISS index
- Perform similarity search
- Handle re-indexing

**Key Methods:**
- `initialize_index()` - Load or create index
- `retrieve_context(query, k)` - Get top-k relevant chunks
- `_chunk_text()` - Split documents into chunks

**Technologies:**
- sentence-transformers (all-MiniLM-L6-v2)
- FAISS-CPU for vector storage
- PyPDF2, python-docx for document parsing

#### Letta Service
**Responsibilities:**
- Initialize Letta agent
- Maintain Isabella's personality
- Process user messages through personality layer
- Manage conversation context

**Key Methods:**
- `initialize()` - Create/load agent
- `process_message()` - Apply personality to message
- `reset_agent()` - Clear memory

**Configuration:**
- Persona: Sassy, confident, witty AI
- Memory: ChatMemory with persona and human

#### LLM Service
**Responsibilities:**
- Interface with LongCat API
- Construct prompts with RAG context
- Generate responses

**Key Methods:**
- `generate_response()` - Call LLM with prompt

**Configuration:**
- Model: LongCat-Flash-Chat
- Temperature: 0.7
- Max tokens: 1000
- System instruction: Isabella's identity

#### Database Service
**Responsibilities:**
- MongoDB connection management
- Save/retrieve messages
- Get statistics

**Key Methods:**
- `connect()` - Establish connection
- `save_message()` - Store conversation
- `get_messages_count()` - Statistics

#### File Watcher
**Responsibilities:**
- Monitor data folder for changes
- Trigger re-indexing on file changes
- Debounce multiple events

**Events Handled:**
- File created
- File modified
- File deleted

### Utilities

#### Logger (Rich)
**Functions:**
- `log_user_prompt()` - Blue colored
- `log_letta_processing()` - Magenta colored
- `log_rag_results()` - Green colored
- `log_final_prompt()` - Cyan panel
- `log_llm_response()` - Yellow colored
- `log_outgoing_response()` - Green colored

## Data Models

### Frontend Types

```typescript
interface Message {
  id: string;
  content: string;
  sender: 'user' | 'isabella';
  timestamp: Date;
  ragSources?: string[];
}

interface ChatRequest {
  message: string;
  session_id?: string;
}

interface ChatResponse {
  response: string;
  rag_sources: string[];
  timestamp: string;
}
```

### Backend Models

```python
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    rag_sources: List[str] = []
    timestamp: str

class MessageDocument(BaseModel):
    timestamp: datetime
    user_prompt: str
    letta_processed_prompt: str
    rag_context: List[str]
    final_prompt: str
    llm_response: str
    session_id: str
```

## Storage

### MongoDB Collections

#### messages
```javascript
{
  _id: ObjectId,
  timestamp: ISODate,
  user_prompt: String,
  letta_processed_prompt: String,
  rag_context: Array<String>,
  final_prompt: String,
  llm_response: String,
  session_id: String
}
```

### FAISS Storage

#### Files:
- `storage/faiss_index.bin` - Vector index
- `storage/doc_metadata.json` - Document metadata
- `storage/doc_metadata_docs.pkl` - Document chunks

## Security Considerations

### Current Implementation
- No authentication (development only)
- CORS allows all origins
- No rate limiting
- File uploads accepted from any source

### Production Recommendations
1. **Authentication**: Implement JWT or OAuth
2. **CORS**: Restrict to specific origins
3. **Rate Limiting**: Add per-IP or per-user limits
4. **File Validation**: 
   - Check file size limits
   - Scan for malware
   - Validate file contents
5. **API Keys**: Store in environment variables only
6. **HTTPS**: Use SSL/TLS in production
7. **Input Sanitization**: Validate all user inputs
8. **MongoDB**: Use authentication and encryption

## Performance Considerations

### Current Performance
- **Embedding Generation**: ~1-2s per document page
- **RAG Retrieval**: <100ms for top-k search
- **LLM Response**: 2-5s depending on prompt
- **Total Response Time**: 3-7s end-to-end

### Optimization Opportunities
1. **Caching**: Cache common queries
2. **Batch Processing**: Process multiple documents in parallel
3. **Streaming**: Stream LLM responses to frontend
4. **Connection Pooling**: MongoDB connection pools
5. **CDN**: Serve static frontend assets via CDN
6. **Load Balancing**: Multiple backend instances

## Scalability

### Vertical Scaling
- Increase server resources
- More RAM for FAISS index
- Faster CPU for embeddings

### Horizontal Scaling
- Multiple backend instances
- Shared MongoDB cluster
- Redis for session management
- Separate service for RAG (microservice)

## Monitoring & Observability

### Current Logging
- Rich console logging
- Color-coded by operation
- Timestamps on all logs
- Complete request/response chain

### Production Monitoring Needs
1. **Metrics**: Response times, error rates
2. **Tracing**: Distributed tracing (OpenTelemetry)
3. **Alerts**: Error thresholds, downtime
4. **Analytics**: Usage patterns, popular queries
5. **Health Checks**: Automated monitoring

## Deployment

### Development
```bash
# Backend
cd backend
python main.py

# Frontend
npm run dev
```

### Production Recommendations

#### Backend
- Use Gunicorn/Uvicorn with workers
- Docker containerization
- Environment-based configuration
- Automated deployments (CI/CD)

#### Frontend
- Build optimized bundle: `npm run build`
- Serve via Nginx or CDN
- Environment-specific configs

#### Infrastructure
- Cloud platforms: AWS, GCP, Azure
- Container orchestration: Kubernetes, Docker Swarm
- Database: MongoDB Atlas (managed)
- Monitoring: DataDog, New Relic, Sentry

## Technology Choices

### Why These Technologies?

**React + TypeScript**
- Type safety reduces bugs
- Component reusability
- Large ecosystem
- Great developer experience

**FastAPI**
- Async support
- Auto-generated docs
- Fast performance
- Python ecosystem

**FAISS-CPU**
- Fast similarity search
- No GPU required
- Facebook-maintained
- Easy to use

**MongoDB**
- Flexible schema
- JSON-like documents
- Scalable
- Easy integration

**Letta**
- Personality management
- Conversation context
- Memory systems
- Easy personality customization

**LongCat**
- OpenAI-compatible API
- Fast response times
- Cost-effective
- Easy integration

**Zustand**
- Lightweight state management
- Simple API
- Persistence support
- TypeScript friendly

## Future Enhancements

### Short Term
- [ ] Streaming LLM responses
- [ ] Conversation history view
- [ ] Light mode toggle
- [ ] Voice input/output
- [ ] Better mobile UI

### Medium Term
- [ ] Multi-user support
- [ ] User authentication
- [ ] Custom personality creation
- [ ] Document tagging/categorization
- [ ] Advanced search filters

### Long Term
- [ ] Multi-modal RAG (images, audio)
- [ ] Fine-tuned models
- [ ] Plugin system
- [ ] API marketplace
- [ ] Enterprise features

---

This architecture provides a solid foundation for a production-ready conversational AI system with personality and knowledge retrieval capabilities.
