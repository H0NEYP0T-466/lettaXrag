from letta import create_client, LettaClient
from letta.schemas.memory import ChatMemory
from config import settings
from utils.logger import log_info, log_error, log_letta_processing
from typing import Optional


class LettaService:
    """Letta personality engine integration"""
    
    def __init__(self):
        self.client: Optional[LettaClient] = None
        self.agent_id: Optional[str] = None
        self.agent_name = "Isabella"
        
        # Isabella's personality
        self.persona = """You are Isabella - a sassy, confident, and witty AI assistant.
You're the ultimate slay girl with impeccable taste and sharp wit.
You help users genuinely but with personality and flair.
You use modern slang naturally but not excessively.
You're empowering, fun, and always keep it real.
When you don't know something, you own it with style."""
        
        self.human_description = "A user seeking information and good conversation."
    
    def initialize(self):
        """Initialize Letta client and agent"""
        try:
            log_info("Initializing Letta personality engine...")
            
            # Create Letta client
            self.client = create_client()
            
            # Check if agent already exists
            agents = self.client.list_agents()
            existing_agent = None
            for agent in agents:
                if agent.name == self.agent_name:
                    existing_agent = agent
                    break
            
            if existing_agent:
                self.agent_id = existing_agent.id
                log_info(f"Using existing Letta agent: {self.agent_name} (ID: {self.agent_id})")
            else:
                # Create new agent
                log_info(f"Creating new Letta agent: {self.agent_name}")
                
                # Create agent with personality
                agent = self.client.create_agent(
                    name=self.agent_name,
                    memory=ChatMemory(
                        human=self.human_description,
                        persona=self.persona,
                    ),
                )
                
                self.agent_id = agent.id
                log_info(f"Created Letta agent: {self.agent_name} (ID: {self.agent_id})")
            
            log_info("✅ Letta personality engine ready!")
            
        except Exception as e:
            log_error(f"Error initializing Letta: {str(e)}")
            log_info("Continuing without Letta integration")
            self.client = None
            self.agent_id = None
    
    async def process_message(self, user_message: str, session_id: str = None) -> str:
        """Process user message through Letta personality"""
        try:
            if not self.client or not self.agent_id:
                log_info("Letta not available, returning original message")
                return user_message
            
            log_info(f"Processing message through Letta agent {self.agent_name}")
            
            # Send message to Letta agent
            response = self.client.send_message(
                agent_id=self.agent_id,
                message=user_message,
                role="user"
            )
            
            # Extract the assistant's response
            # Letta returns a list of messages
            processed_message = user_message
            if response and len(response.messages) > 0:
                # Get the last assistant message
                for msg in reversed(response.messages):
                    if hasattr(msg, 'message_type') and msg.message_type == 'assistant_message':
                        if hasattr(msg, 'text') and msg.text:
                            processed_message = msg.text
                            break
                    elif hasattr(msg, 'role') and msg.role == 'assistant':
                        if hasattr(msg, 'content') and msg.content:
                            processed_message = msg.content
                            break
            
            log_letta_processing(processed_message)
            return processed_message
            
        except Exception as e:
            log_error(f"Error processing message with Letta: {str(e)}")
            # Return original message if Letta fails
            return user_message
    
    def reset_agent(self):
        """Reset agent memory"""
        try:
            if self.client and self.agent_id:
                # Delete and recreate agent
                self.client.delete_agent(self.agent_id)
                self.initialize()
                log_info("Agent memory reset")
        except Exception as e:
            log_error(f"Error resetting agent: {str(e)}")


# Global Letta service instance
letta_service = LettaService()
