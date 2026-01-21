from sqlalchemy import Column, Integer, String, DateTime, Boolean
from models.base import Base  # The base declarative class
from datetime import datetime

# Existing model: ChatMessage
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message = Column(String, nullable=False)

# New model: Organization
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    privileged_tools = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    is_deleted = Column(Boolean, default=False)
    _created_by_id = Column(String, nullable=True)
    _last_updated_by_id = Column(String, nullable=True)