from openai import OpenAI
from config import settings
from utils.logger import log_info, log_error, log_llm_response


class LLMService:
    """LongCat LLM integration using OpenAI client"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.longcat_api_key,
            base_url="https://api.longcat.chat/openai"
        )
        self.model = "LongCat-Flash-Chat"
        self.system_instruction = (
            "Your name is Isabella. You are a sassy, confident AI assistant who helps users "
            "with their questions using retrieved knowledge."
        )
    
    async def generate_response(
        self,
        prompt: str,
        rag_context: list = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate response from LLM"""
        try:
            # Construct messages
            messages = [
                {"role": "system", "content": self.system_instruction}
            ]
            
            # Add RAG context if available
            if rag_context and len(rag_context) > 0:
                context_text = "Here is some relevant information to help answer the question:\n\n"
                for i, ctx in enumerate(rag_context, 1):
                    context_text += f"[Source {i}]\n{ctx}\n\n"
                messages.append({"role": "system", "content": context_text})
            
            # Add user prompt
            messages.append({"role": "user", "content": prompt})
            
            log_info(f"Sending request to LongCat LLM (model: {self.model})")
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            llm_response = response.choices[0].message.content
            log_llm_response(llm_response)
            
            return llm_response
            
        except Exception as e:
            log_error(f"Error calling LLM: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."


# Global LLM service instance
llm_service = LLMService()
