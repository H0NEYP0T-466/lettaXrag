from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from datetime import datetime

custom_theme = Theme({
    "user": "bold blue",
    "letta": "bold magenta",
    "rag": "bold green",
    "llm": "bold yellow",
    "info": "bold cyan",
    "success": "bold green",
    "error": "bold red",
})

console = Console(theme=custom_theme)


def log_user_prompt(message: str):
    """Log incoming user prompt"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.log(f"[user]📥 USER PROMPT [{timestamp}][/user]", message)


def log_letta_processing(output: str):
    """Log Letta personality processing"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.log(f"[letta]🎭 LETTA PROCESSING [{timestamp}][/letta]", output)


def log_rag_results(results: list):
    """Log RAG similarity retrieval results"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.log(f"[rag]📚 RAG SIMILARITY RESULTS [{timestamp}][/rag]")
    for i, result in enumerate(results, 1):
        console.print(f"  {i}. {result[:100]}..." if len(result) > 100 else f"  {i}. {result}")


def log_final_prompt(prompt: str):
    """Log final constructed prompt sent to LLM"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(prompt, title=f"🚀 FINAL PROMPT TO LLM [{timestamp}]", border_style="cyan"))


def log_llm_response(response: str):
    """Log LLM raw response"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.log(f"[llm]🤖 LLM RESPONSE [{timestamp}][/llm]", response)


def log_outgoing_response(response: str):
    """Log outgoing response to frontend"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.log(f"[success]✅ OUTGOING RESPONSE [{timestamp}][/success]", response[:200] + "..." if len(response) > 200 else response)


def log_info(message: str):
    """Log general information"""
    console.log(f"[info]ℹ️  {message}[/info]")


def log_success(message: str):
    """Log success message"""
    console.log(f"[success]✅ {message}[/success]")


def log_error(message: str):
    """Log error message"""
    console.log(f"[error]❌ {message}[/error]")
