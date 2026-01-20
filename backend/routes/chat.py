from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import ChatRequest, ChatResponse, HealthResponse, StatsResponse
from services.db_service import db_service
from services.rag_service import rag_service
from services.letta_service import letta_service
from services.llm_service import llm_service
from utils.logger import (
    log_user_prompt, log_rag_results, log_final_prompt,
    log_outgoing_response, log_info, log_error
)
from datetime import datetime
import uuid
import os
from config import settings
from pathlib import Path

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Log incoming user prompt
        log_user_prompt(request.message)
        
        # Process message through Letta personality engine
        letta_processed = await letta_service.process_message(
            request.message,
            session_id
        )
        
        # Retrieve relevant context from RAG
        rag_context = rag_service.retrieve_context(request.message, k=3)
        log_rag_results(rag_context)
        
        # Construct final prompt
        final_prompt = letta_processed
        log_final_prompt(final_prompt)
        
        # Generate response from LLM
        llm_response = await llm_service.generate_response(
            prompt=final_prompt,
            rag_context=rag_context
        )
        
        # Prepare response
        response_text = llm_response
        log_outgoing_response(response_text)
        
        # Save to database
        message_data = {
            "timestamp": datetime.utcnow(),
            "user_prompt": request.message,
            "letta_processed_prompt": letta_processed,
            "rag_context": rag_context,
            "final_prompt": final_prompt,
            "llm_response": llm_response,
            "session_id": session_id
        }
        await db_service.save_message(message_data)
        
        # Get source filenames
        rag_sources = []
        if rag_context:
            # Extract unique source filenames from metadata
            for ctx in rag_context[:3]:  # Limit to top 3
                # Find matching metadata
                for meta in rag_service.metadata:
                    if rag_service.documents[rag_service.metadata.index(meta)] == ctx:
                        source = meta.get('source', 'Unknown')
                        if source not in rag_sources:
                            rag_sources.append(source)
                        break
        
        return ChatResponse(
            response=response_text,
            rag_sources=rag_sources,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        log_error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    mongodb_status = "connected" if db_service.is_connected() else "disconnected"
    faiss_status = "ready" if rag_service.index is not None else "not initialized"
    
    overall_status = "healthy" if mongodb_status == "connected" and faiss_status == "ready" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        mongodb=mongodb_status,
        faiss=faiss_status,
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file to data folder"""
    try:
        # Validate file type
        allowed_extensions = ['.txt', '.md', '.pdf', '.docx']
        file_ext = Path(file.filename).suffix
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save file to data folder
        file_path = os.path.join(settings.data_folder, file.filename)
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        log_info(f"File uploaded: {file.filename}")
        
        # Trigger re-indexing
        log_info("Triggering re-indexing...")
        rag_service.initialize_index(force_rebuild=True)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "status": "indexed"
        }
        
    except Exception as e:
        log_error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics"""
    try:
        message_count = await db_service.get_messages_count()
        rag_stats = rag_service.get_stats()
        
        return StatsResponse(
            message_count=message_count,
            indexed_documents=rag_stats['indexed_documents'],
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        log_error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
