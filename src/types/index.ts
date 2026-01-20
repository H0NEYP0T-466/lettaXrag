export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'isabella';
  timestamp: Date;
  ragSources?: string[];
}

export interface ChatResponse {
  response: string;
  rag_sources: string[];
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface HealthResponse {
  status: string;
  mongodb: string;
  faiss: string;
  timestamp: string;
}

export interface StatsResponse {
  message_count: number;
  indexed_documents: number;
  timestamp: string;
}
