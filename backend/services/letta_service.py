try:
    from letta_client import Letta
    from letta import ChatMemory
    LETTA_AVAILABLE = True
except ImportError:
    LETTA_AVAILABLE = False
    Letta = None
    ChatMemory = None

from config import settings
from utils.logger import log_info, log_error, log_letta_processing
from typing import Optional


class LettaService:
    """Letta personality engine integration"""
    
    def __init__(self):
        self.client: Optional[Letta] = None
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
            if not LETTA_AVAILABLE:
                log_info("⚠️  Letta library not installed")
                log_info("Isabella will work without personality processing")
                self.client = None
                self.agent_id = None
                return
            
            log_info("Initializing Letta personality engine...")
            
            # Create Letta client with configured base URL
            # By default (from config.py), uses local server at http://localhost:8283
            # Can be overridden via LETTA_BASE_URL environment variable
            client_kwargs = {}
            if settings.letta_base_url:
                client_kwargs['base_url'] = settings.letta_base_url
                log_info(f"✅ Connecting to Letta server: {settings.letta_base_url}")
            if settings.letta_api_key:
                client_kwargs['token'] = settings.letta_api_key
                log_info("✅ Using Letta API key for authentication")
            
            self.client = Letta(**client_kwargs)
            
            # Check if agent already exists
            agents_response = self.client.agents.list(name=self.agent_name)
            existing_agent = None
            
            # Check if any agents match our name
            if hasattr(agents_response, 'data') and agents_response.data:
                for agent in agents_response.data:
                    if agent.name == self.agent_name:
                        existing_agent = agent
                        break
            
            if existing_agent:
                self.agent_id = existing_agent.id
                log_info(f"Using existing Letta agent: {self.agent_name} (ID: {self.agent_id})")
            else:
                # Create new agent with personality
                log_info(f"Creating new Letta agent: {self.agent_name}")
                
                # Create memory blocks for the agent
                memory_blocks = [
                    {
                        "label": "persona",
                        "value": self.persona,
                        "template": False
                    },
                    {
                        "label": "human",
                        "value": self.human_description,
                        "template": False
                    }
                ]
                
                agent = self.client.agents.create(
                    name=self.agent_name,
                    memory_blocks=memory_blocks,
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
            
            # Send message to Letta agent using the new API
            response = self.client.agents.messages.create(
                agent_id=self.agent_id,
                input=user_message,
            )
            
            # Extract the assistant's response
            # Letta returns a response object with messages
            processed_message = user_message
            if hasattr(response, 'messages') and response.messages:
                # Get the last assistant message
                for msg in reversed(response.messages):
                    # Check for assistant messages
                    if hasattr(msg, 'role') and msg.role == 'assistant':
                        if hasattr(msg, 'text') and msg.text:
                            processed_message = msg.text
                            break
                    # Also check for message_type attribute
                    elif hasattr(msg, 'message_type') and 'assistant' in str(msg.message_type).lower():
                        if hasattr(msg, 'text') and msg.text:
                            processed_message = msg.text
                            break
                    # Check for content attribute
                    elif hasattr(msg, 'content') and msg.content:
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
                self.client.agents.delete(self.agent_id)
                self.initialize()
                log_info("Agent memory reset")
        except Exception as e:
            log_error(f"Error resetting agent: {str(e)}")


# Global Letta service instance
letta_service = LettaService()
