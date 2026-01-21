try:
    from letta_client import Letta
    LETTA_AVAILABLE = True
except ImportError: 
    LETTA_AVAILABLE = False
    Letta = None

from config import settings
from utils.logger import log_info, log_error, log_letta_processing
from typing import Optional


class LettaService:
    def __init__(self):
        self.client = None
        self. agent_id = None
        self.agent_name = "Isabella"
        self.persona = """You are Isabella - a sassy, confident, and witty AI assistant. 
You're the ultimate slay girl with impeccable taste and sharp wit. 
You help users genuinely but with personality and flair.
You use modern slang naturally but not excessively.
You're empowering, fun, and always keep it real.
When you don't know something, you own it with style. 

IMPORTANT: You have persistent memory.  Remember details about users like their name,
preferences, past conversations, and anything they share with you."""
        self.human_description = "A user seeking information and good conversation."

    def initialize(self):
        try:
            if not LETTA_AVAILABLE: 
                log_info("Letta library not installed - running without memory")
                self.client = None
                self. agent_id = None
                return

            log_info("Initializing Letta personality engine with memory...")

            client_kwargs = {}
            if settings.letta_base_url:
                client_kwargs['base_url'] = settings. letta_base_url
                log_info(f"Configuring Letta client for:  {settings.letta_base_url}")
            if hasattr(settings, 'letta_api_key') and settings.letta_api_key: 
                client_kwargs['token'] = settings.letta_api_key

            self.client = Letta(**client_kwargs)
            log_info(f"Connected to Letta server:  {settings.letta_base_url or 'default'}")

            agents_response = self.client.agents.list(name=self.agent_name)
            existing_agent = None

            if hasattr(agents_response, '__iter__'):
                for agent in agents_response:
                    if hasattr(agent, 'name') and agent.name == self. agent_name:
                        existing_agent = agent
                        break

            if existing_agent: 
                self.agent_id = existing_agent.id
                log_info(f"Using existing Letta agent: {self.agent_name} (ID: {self.agent_id})")
            else:
                log_info(f"Creating new Letta agent: {self.agent_name}")

                memory_blocks = [
                    {"label": "persona", "value": self.persona, "template": False},
                    {"label": "human", "value": self.human_description, "template": False}
                ]

                agent = self.client.agents.create(
                    name=self.agent_name,
                    llm_config={
                        "model": "LongCat-Flash-Chat",
                        "model_endpoint_type": "openai",
                        "model_endpoint": "https://api.longcat.chat/openai",
                        "context_window": 32000,
                        "put_inner_thoughts_in_kwargs": True
                    },
                    embedding_config={
                        "embedding_model": "text-embedding-3-small",
                        "embedding_endpoint_type": "openai",
                        "embedding_endpoint":  "https://api.openai.com/v1",
                        "embedding_dim": 1536
                    },
                    memory_blocks=memory_blocks,
                )

                self.agent_id = agent.id
                log_info(f"Created Letta agent:  {self.agent_name} (ID: {self.agent_id})")

            log_info("Letta personality engine with memory ready!")

        except Exception as e: 
            log_error(f"Error initializing Letta: {str(e)}")
            log_info("Continuing without Letta integration")
            self.client = None
            self.agent_id = None

    async def process_message(self, user_message, session_id=None):
        """Process user message through Letta with memory."""
        try:
            if not self.client or not self.agent_id:
                log_info("Letta not available, returning original message")
                return user_message

            log_info("Processing message through Letta agent (with memory)")

            response = self.client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content":  user_message}]
            )

            assistant_response = None
            if hasattr(response, 'messages') and response.messages:
                for msg in response.messages:
                    if hasattr(msg, 'message_type'):
                        msg_type = str(msg.message_type).lower()
                        if 'assistant' in msg_type or 'response' in msg_type:
                            if hasattr(msg, 'assistant_message') and msg.assistant_message:
                                assistant_response = msg. assistant_message
                                break
                            elif hasattr(msg, 'content') and msg.content:
                                assistant_response = msg.content
                                break
                            elif hasattr(msg, 'text') and msg.text:
                                assistant_response = msg.text
                                break

            if assistant_response:
                log_letta_processing(f"Isabella (with memory): {assistant_response[:100]}...")
                return assistant_response
            else:
                log_info("No assistant response found in Letta response")
                return user_message

        except Exception as e:
            log_error(f"Error processing message with Letta: {str(e)}")
            return user_message

    async def process_with_memory(self, user_message, rag_context=None, user_id="default_user"):
        """Process with RAG context included."""
        full_message = user_message
        if rag_context and len(rag_context) > 0:
            context_text = "\n\n---\nRelevant information from knowledge base:\n"
            for i, ctx in enumerate(rag_context, 1):
                context_text += f"\n[Source {i}]:  {ctx}\n"
            context_text += "---\n\nUse this information to help answer the user's question."
            full_message = f"{user_message}{context_text}"

        return await self.process_message(full_message)

    def reset_agent(self):
        """Reset agent memory."""
        try:
            if self.client and self.agent_id:
                self.client.agents.delete(self.agent_id)
                self.agent_id = None
                self.initialize()
                log_info("Agent memory reset")
        except Exception as e:
            log_error(f"Error resetting agent: {str(e)}")


letta_service = LettaService()