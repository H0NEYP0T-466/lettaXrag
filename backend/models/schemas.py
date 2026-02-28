from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    model: Optional[str] = "longcat"
    use_rag: Optional[bool] = True
    use_letta: Optional[bool] = True


class ChatResponse(BaseModel):
    response: str
    rag_sources: List[str] = []
    timestamp: str


class MessageDocument(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_prompt: str
    letta_processed_prompt: str
    rag_context: List[str]
    final_prompt: str
    llm_response: str
    session_id: str


class HealthResponse(BaseModel):
    status: str
    mongodb: str
    faiss: str
    timestamp: str


class StatsResponse(BaseModel):
    message_count: int
    indexed_documents: int
    timestamp: str
