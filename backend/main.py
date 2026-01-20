from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.chat import router as chat_router
from services.db_service import db_service
from services.rag_service import rag_service
from services.letta_service import letta_service
from utils.logger import log_info, log_success, log_error
from utils.file_watcher import FileWatcher
from config import settings
import uvicorn


# File watcher instance
file_watcher = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    log_info("🚀 Starting LettaXRAG backend...")
    
    try:
        # Initialize MongoDB
        await db_service.connect()
        
        # Initialize RAG service
        log_info("Initializing RAG service...")
        rag_service.initialize_index()
        
        # Initialize Letta service
        letta_service.initialize()
        
        # Start file watcher
        global file_watcher
        file_watcher = FileWatcher(
            settings.data_folder,
            lambda: rag_service.initialize_index(force_rebuild=True)
        )
        file_watcher.start()
        
        log_success("✅ LettaXRAG backend ready!")
        
    except Exception as e:
        log_error(f"Error during startup: {str(e)}")
    
    yield
    
    # Shutdown
    log_info("Shutting down LettaXRAG backend...")
    
    # Stop file watcher
    if file_watcher:
        file_watcher.stop()
    
    # Disconnect from MongoDB
    await db_service.disconnect()
    
    log_info("👋 Goodbye!")


# Create FastAPI app
app = FastAPI(
    title="LettaXRAG API",
    description="Conversational AI with RAG and Personality Management",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LettaXRAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
