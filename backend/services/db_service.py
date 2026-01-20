from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import settings
from utils.logger import log_info, log_error, log_success
from typing import Dict, Any, List
from datetime import datetime


class DatabaseService:
    """MongoDB database operations"""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.messages_collection = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.db = self.client.lettaXrag
            self.messages_collection = self.db.messages
            
            # Test connection
            await self.client.admin.command('ping')
            log_success(f"Connected to MongoDB: {settings.mongodb_uri}")
        except Exception as e:
            log_error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            log_info("Disconnected from MongoDB")
    
    async def save_message(self, message_data: Dict[str, Any]):
        """Save a message to the database"""
        try:
            result = await self.messages_collection.insert_one(message_data)
            log_success(f"Message saved with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            log_error(f"Failed to save message: {str(e)}")
            raise
    
    async def get_messages_count(self) -> int:
        """Get total message count"""
        try:
            count = await self.messages_collection.count_documents({})
            return count
        except Exception as e:
            log_error(f"Failed to get message count: {str(e)}")
            return 0
    
    async def get_messages_by_session(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent messages for a session"""
        try:
            cursor = self.messages_collection.find(
                {"session_id": session_id}
            ).sort("timestamp", -1).limit(limit)
            messages = await cursor.to_list(length=limit)
            return messages
        except Exception as e:
            log_error(f"Failed to get messages: {str(e)}")
            return []
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            if self.client:
                # Synchronous check
                sync_client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
                sync_client.admin.command('ping')
                sync_client.close()
                return True
        except:
            pass
        return False


# Global database service instance
db_service = DatabaseService()
