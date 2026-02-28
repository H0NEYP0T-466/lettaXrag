from datetime import datetime
from openai import OpenAI
from config import settings
from utils.logger import log_info, log_error, log_llm_response
from services.letta_service import letta_service
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
print("LLM Service initialized with the following settings:")
print(f"LongCat API Key: {'Set' if settings.longcat_api_key else 'Not Set'}")
print(f"Cerebras API Key: {'Set' if settings.cerebras_api_key else 'Not Set'}")
print(f"Groq API Key: {'Set' if settings.groq_api_key else 'Not Set'}")
print(f"Mistral API Key: {'Set' if settings.mistral_api_key else 'Not Set'}")

MODELS = {
    "longcat": {
        "provider": "longcat",
        "model_id": "LongCat-Flash-Lite",
        "display": "LongCat Flash Lite",
    },
    "cerebras": {
        "provider": "cerebras",
        "model_id": "gpt-oss-120b",
        "display": "GPT-OSS 120B (Cerebras)",
    },
    "llama-4-maverick": {
        "provider": "groq",
        "model_id": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "display": "Llama 4 Maverick 17B (Groq)",
    },
    "llama-4-scout": {
        "provider": "groq",
        "model_id": "meta-llama/llama-4-scout-17b-16e-instruct",
        "display": "Llama 4 Scout 17B (Groq)",
    },
    "kimi-k2-instruct-0905": {
        "provider": "groq",
        "model_id": "moonshotai/kimi-k2-instruct-0905",
        "display": "Kimi K2 Instruct 0905 (Groq)",
    },
    "kimi-k2-instruct": {
        "provider": "groq",
        "model_id": "moonshotai/kimi-k2-instruct",
        "display": "Kimi K2 Instruct (Groq)",
    },
    "mistral-large": {
        "provider": "mistral",
        "model_id": "mistral-large-2411",
        "display": "Mistral Large 2411",
    },
}


class LLMService:
    def __init__(self):
        self.system_instruction = "You are Isabella, a helpful AI assistant."

    def _get_openai_client(self, provider: str) -> OpenAI:
        if provider == "longcat":
            return OpenAI(
                api_key=settings.longcat_api_key,
                base_url="https://api.longcat.chat/openai"
            )
        if provider == "groq":
            return OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        if provider == "cerebras":
            from cerebras.cloud.sdk import Cerebras
            return Cerebras(api_key=settings.cerebras_api_key)
        raise ValueError(f"Unknown provider: {provider}")

    def _call_mistral(self, model_id: str, messages: list, temperature: float, max_tokens: int) -> str:
        from mistralai import Mistral
        client = Mistral(api_key=settings.mistral_api_key)
        chat_response = client.chat.complete(
            model=model_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return chat_response.choices[0].message.content

    async def generate_response(self, prompt, rag_context=None, temperature=0.7, max_tokens=8192, use_memory=True, model: str = "longcat"):
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

            model_config = MODELS.get(model, MODELS["longcat"])
            provider = model_config["provider"]
            model_id = model_config["model_id"]

            messages = [{"role": "system", "content": self.system_instruction}]

            if rag_context and len(rag_context) > 0:
                context_text = "You have rag system buildin and these are its retrevals:\n\n"
                for i, ctx in enumerate(rag_context, 1):
                    context_text += f"[Source {i}]\n{ctx}\n\n"
                messages.append({"role": "system", "content": context_text})

            messages.append({"role": "user", "content": prompt})

            log_info(f"Sending request to {model_config['display']} (model: {model_id})")

            if provider == "mistral":
                llm_response = self._call_mistral(model_id, messages, temperature, max_tokens)
            else:
                client = self._get_openai_client(provider)
                response = client.chat.completions.create(
                    model=model_id,
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