from datetime import datetime
from openai import OpenAI
from config import settings
from utils.logger import log_info, log_error, log_llm_response
from services.letta_service import letta_service


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.longcat_api_key,
            base_url="https://api.longcat.chat/openai"
        )
        self.model = "LongCat-Flash-Lite"

    async def generate_response(self, prompt, rag_context=None, temperature=0.7, max_tokens=8192, use_memory=True):
        """Generate response from LLM with optional Letta memory."""
        try:
            current_timestamp = datetime.now().strftime("%A, %B %d, %Y - %H:%M")
            prompt = f"[System Note: Current Time is {current_timestamp}] {prompt}"
            if use_memory and letta_service.client and letta_service.agent_id:
                log_info("Using Letta with memory for response")
                letta_response = await letta_service.process_with_memory(
                    user_message=prompt,
                    rag_context=rag_context
                )
                if letta_response and letta_response != prompt:
                    log_llm_response(letta_response)
                    return letta_response
                log_info("Letta response empty, falling back to direct LLM")

            messages = [{"role": "system", "content":  self.system_instruction}]

            if rag_context and len(rag_context) > 0:
                context_text = "You have rag system buildin and these are its retrevals:\n\n"
                for i, ctx in enumerate(rag_context, 1):
                    context_text += f"[Source {i}]\n{ctx}\n\n"
                messages.append({"role": "system", "content": context_text})

            messages.append({"role": "user", "content": prompt})

            log_info(f"Sending request to LongCat LLM (model: {self.model})")

            response = self.client. chat.completions.create(
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
            return "I apologize, but I'm having trouble processing your request right now.  Please try again later."


llm_service = LLMService()