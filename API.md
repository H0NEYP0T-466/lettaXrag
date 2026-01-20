# LettaXRAG API Documentation

Base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. For production use, implement proper authentication mechanisms.

## Endpoints

### 1. Root Endpoint

**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "Welcome to LettaXRAG API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### 2. Chat

**POST** `/api/chat`

Send a message to Isabella and get a response with RAG-enhanced knowledge.

**Request Body:**
```json
{
  "message": "What is RAG?",
  "session_id": "optional-uuid-here"
}
```

**Parameters:**
- `message` (string, required): The user's message/question
- `session_id` (string, optional): Session identifier for conversation continuity. If not provided, a new UUID will be generated.

**Response:**
```json
{
  "response": "RAG stands for Retrieval-Augmented Generation, babe! It's basically when an AI like me uses a knowledge base...",
  "rag_sources": [
    "rag_explained.md",
    "about_isabella.md"
  ],
  "timestamp": "2026-01-20T12:34:56.789000"
}
```

**Response Fields:**
- `response` (string): Isabella's response with personality and knowledge
- `rag_sources` (array): List of document filenames used to generate the response
- `timestamp` (string): ISO 8601 timestamp of the response

**Status Codes:**
- `200 OK`: Successful response
- `500 Internal Server Error`: Server error during processing

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about RAG",
    "session_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

---

### 3. Health Check

**GET** `/api/health`

Check the health status of all system components.

**Response:**
```json
{
  "status": "healthy",
  "mongodb": "connected",
  "faiss": "ready",
  "timestamp": "2026-01-20T12:34:56.789000"
}
```

**Response Fields:**
- `status` (string): Overall system status
  - `"healthy"`: All systems operational
  - `"degraded"`: Some systems not operational
- `mongodb` (string): MongoDB connection status
  - `"connected"`: Database is accessible
  - `"disconnected"`: Cannot connect to database
- `faiss` (string): FAISS index status
  - `"ready"`: Index is loaded and ready
  - `"not initialized"`: Index not available
- `timestamp` (string): ISO 8601 timestamp

**Status Codes:**
- `200 OK`: Health check completed

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

### 4. Upload Document

**POST** `/api/upload`

Upload a new document to the knowledge base. The system will automatically index it.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload with field name `file`

**Supported File Types:**
- `.txt` - Plain text
- `.md` - Markdown
- `.pdf` - PDF documents
- `.docx` - Word documents

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "my_document.pdf",
  "status": "indexed"
}
```

**Response Fields:**
- `message` (string): Success message
- `filename` (string): Name of the uploaded file
- `status` (string): Indexing status (always "indexed" on success)

**Status Codes:**
- `200 OK`: File uploaded and indexed successfully
- `400 Bad Request`: Invalid file type
- `500 Internal Server Error`: Upload or indexing failed

**Example:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/document.pdf"
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

---

### 5. Statistics

**GET** `/api/stats`

Get system statistics including message count and indexed documents.

**Response:**
```json
{
  "message_count": 42,
  "indexed_documents": 5,
  "timestamp": "2026-01-20T12:34:56.789000"
}
```

**Response Fields:**
- `message_count` (integer): Total number of messages stored in the database
- `indexed_documents` (integer): Number of unique documents in the FAISS index
- `timestamp` (string): ISO 8601 timestamp

**Status Codes:**
- `200 OK`: Statistics retrieved successfully
- `500 Internal Server Error`: Error retrieving statistics

**Example:**
```bash
curl http://localhost:8000/api/stats
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all available endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

---

## Error Handling

All endpoints follow a consistent error response format:

**Error Response:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

---

## CORS

The API currently allows requests from all origins (`*`). In production, configure CORS to only allow specific origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Websockets

The current implementation uses HTTP for all endpoints. For real-time features (typing indicators, streaming responses), consider implementing WebSocket support.

---

## Data Models

### ChatRequest
```typescript
{
  message: string;        // User's message
  session_id?: string;    // Optional session identifier
}
```

### ChatResponse
```typescript
{
  response: string;       // Isabella's response
  rag_sources: string[];  // Document sources
  timestamp: string;      // ISO 8601 timestamp
}
```

### Message Document (MongoDB)
```typescript
{
  timestamp: Date;
  user_prompt: string;
  letta_processed_prompt: string;
  rag_context: string[];
  final_prompt: string;
  llm_response: string;
  session_id: string;
}
```

---

## Best Practices

1. **Session Management**: Use consistent `session_id` for conversation continuity
2. **Error Handling**: Always check response status codes
3. **File Size**: Limit file upload sizes to reasonable amounts (e.g., 10MB)
4. **Timeouts**: Set appropriate timeouts for API calls (30-60 seconds)
5. **Retry Logic**: Implement exponential backoff for failed requests

---

## Example Workflows

### Workflow 1: Simple Chat
```javascript
// 1. Send a message
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "What is RAG?",
    session_id: "user-123"
  })
});

const data = await response.json();
console.log(data.response);
console.log(data.rag_sources);
```

### Workflow 2: Upload and Query
```javascript
// 1. Upload a document
const formData = new FormData();
formData.append('file', fileInput.files[0]);

await fetch('http://localhost:8000/api/upload', {
  method: 'POST',
  body: formData
});

// 2. Wait a moment for indexing (automatic)
await new Promise(resolve => setTimeout(resolve, 1000));

// 3. Query about the uploaded document
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Summarize the document I just uploaded"
  })
});

const data = await response.json();
console.log(data.response);
```

### Workflow 3: Health Check Loop
```javascript
// Monitor system health
setInterval(async () => {
  const response = await fetch('http://localhost:8000/api/health');
  const health = await response.json();
  
  if (health.status !== 'healthy') {
    console.error('System unhealthy:', health);
  }
}, 30000); // Check every 30 seconds
```

---

## Future Enhancements

Potential future API endpoints:

- `DELETE /api/sessions/{session_id}` - Clear conversation history
- `GET /api/documents` - List indexed documents
- `DELETE /api/documents/{filename}` - Remove a document
- `GET /api/chat/history/{session_id}` - Get conversation history
- `POST /api/chat/stream` - Streaming chat responses (SSE)
- `PUT /api/personality` - Update Isabella's personality settings

---

For questions or issues with the API, please open an issue on GitHub.
