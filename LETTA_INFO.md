# Letta Integration Guide

## Table of Contents
1. [What is Letta?](#what-is-letta)
2. [How Letta Works](#how-letta-works)
3. [System Instructions & Persona](#system-instructions--persona)
4. [Implementation in LettaXRAG](#implementation-in-lettaxrag)
5. [Configuration](#configuration)
6. [Usage Examples](#usage-examples)
7. [Troubleshooting](#troubleshooting)

---

## What is Letta?

**Letta** (formerly MemGPT) is a personality and memory management system for Large Language Models (LLMs). It enables AI assistants to maintain:

- **Persistent Personality**: Consistent character traits and communication style
- **Long-term Memory**: Conversation history across sessions
- **Context Management**: Intelligent handling of conversation context
- **Agent State**: Stateful interactions that remember previous conversations

### Key Features

- 🎭 **Personality Engine**: Define and maintain consistent AI personas
- 💾 **Memory Management**: Store and retrieve conversation history
- 🔄 **Context Handling**: Smart context window management
- 🌐 **Multi-session Support**: Track different conversation threads
- 🔌 **API Integration**: Easy integration with various LLM providers

---

## How Letta Works

### Architecture Overview

```
User Message
    ↓
Letta Agent (Personality Layer)
    ↓
Memory Retrieval (Past Context)
    ↓
Persona Application (Character Traits)
    ↓
Processed Message
    ↓
LLM (Language Model)
    ↓
Response
```

### Core Components

#### 1. **Agent**
- The central entity that processes messages
- Contains personality definition and memory
- Maintains conversation state

#### 2. **Memory System**
- **Human Description**: Information about the user
- **Persona**: AI's character and personality traits
- **Conversation History**: Past messages and context

#### 3. **Message Processing**
1. User sends a message
2. Letta agent retrieves relevant memory
3. Applies personality filters
4. Forwards processed message to LLM
5. Stores response in memory
6. Returns response to user

---

## System Instructions & Persona

### Does Letta Need Different System Instructions?

**Yes and No** - Here's the distinction:

#### LLM System Instructions (Base Level)
```python
# Traditional LLM prompt
system_prompt = """You are a helpful AI assistant.
Answer questions accurately and concisely."""
```

#### Letta Persona (Personality Layer)
```python
# Letta personality definition
persona = """You are Isabella - a sassy, confident AI assistant.
You're witty, empowering, and keep it real.
You use modern slang naturally but not excessively."""
```

### The Difference

- **LLM Instructions**: Define capabilities, knowledge boundaries, and response format
- **Letta Persona**: Define personality, tone, communication style, and character

### Why Use Both?

1. **LLM Instructions** → What the AI can do (technical capabilities)
2. **Letta Persona** → How the AI behaves (personality traits)

### Best Practice: Layered Approach

```
┌─────────────────────────────┐
│   Letta Persona Layer       │ ← Personality & Style
│  (Character Traits)         │
├─────────────────────────────┤
│   LLM System Prompt         │ ← Capabilities & Rules
│  (Technical Instructions)   │
├─────────────────────────────┤
│   Base LLM Model            │ ← Core Language Model
└─────────────────────────────┘
```

---

## Implementation in LettaXRAG

### Current Implementation

Located in: `/backend/services/letta_service.py`

**Updated for Letta 0.16.x API:**

```python
# New imports for Letta 0.16.x
try:
    from letta_client import Letta  # Client from letta_client package
    from letta import ChatMemory      # Schemas from letta package
    LETTA_AVAILABLE = True
except ImportError:
    LETTA_AVAILABLE = False

class LettaService:
    def __init__(self):
        self.client = None  # Now uses Letta class instead of LettaClient
        self.agent_id = None
        self.agent_name = "Isabella"
        
        # Isabella's personality definition
        self.persona = """You are Isabella - a sassy, confident, and witty AI assistant.
        You're the ultimate slay girl with impeccable taste and sharp wit.
        You help users genuinely but with personality and flair.
        You use modern slang naturally but not excessively.
        You're empowering, fun, and always keep it real.
        When you don't know something, you own it with style."""
        
        self.human_description = "A user seeking information and good conversation."
```

**Key API Changes in Letta 0.16.x:**
- Client initialization: `Letta()` instead of `create_client()`
- List agents: `client.agents.list(name="name")` instead of `client.list_agents()`
- Create agent: `client.agents.create(name="name", memory_blocks=[...])` instead of `client.create_agent()`
- Send message: `client.agents.messages.create(agent_id="id", input="message")` instead of `client.send_message()`
- Delete agent: `client.agents.delete(agent_id)` instead of `client.delete_agent()`


### Integration Flow

1. **Initialization** (`main.py`)
   ```python
   letta_service.initialize()
   ```

2. **Message Processing** (`routes/chat.py`)
   ```python
   # User message → Letta processing
   letta_processed = await letta_service.process_message(
       request.message,
       session_id
   )
   
   # Letta processed message → RAG context retrieval
   rag_context = rag_service.retrieve_context(letta_processed)
   
   # Final prompt → LLM
   llm_response = await llm_service.generate_response(
       prompt=letta_processed,
       rag_context=rag_context
   )
   ```

3. **Response Flow**
   ```
   User: "What is RAG?"
      ↓
   Letta: Adds personality context and memory
      ↓
   RAG: Retrieves relevant documents
      ↓
   LLM: Generates response with personality and context
      ↓
   Isabella: "Oh honey, RAG is Retrieval-Augmented Generation! 
             Let me break it down for you..."
   ```

---

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Required for LettaXRAG
MONGODB_URI=mongodb://localhost:27017/lettaXrag
LONGCAT_API_KEY=your_longcat_api_key

# Optional - Letta Configuration
LETTA_API_KEY=your_letta_api_key  # If using Letta Cloud
LETTA_BASE_URL=http://localhost:8283  # If using local Letta server

# Other settings
DATA_FOLDER=./data
FAISS_INDEX_PATH=./storage/faiss_index.bin
LOG_LEVEL=DEBUG
```

### Installation

#### Option 1: Install Letta (Recommended for Latest Version)

```bash
cd backend
pip install letta>=0.16.0
```

✅ **Updated:** Now requires Letta 0.16.0 or later with the new API structure.

#### Option 2: Use Without Letta

The system works without Letta installed. Personality is maintained through:
- LLM system prompts in `llm_service.py`
- Consistent persona definition
- MongoDB conversation history

### Customizing Personality

Edit `backend/services/letta_service.py`:

```python
self.persona = """Your custom personality here...

Examples:
- Professional and formal
- Casual and friendly  
- Technical and precise
- Creative and playful
"""
```

---

## Usage Examples

### Example 1: Basic Conversation

**Without Letta:**
```
User: "What is RAG?"
AI: "RAG stands for Retrieval-Augmented Generation. It's a technique..."
```

**With Letta:**
```
User: "What is RAG?"
Isabella: "Ooh girl, RAG is where it's at! 🔥 It stands for Retrieval-Augmented 
          Generation - basically, I pull info from documents to give you the 
          most accurate tea! ☕"
```

### Example 2: Memory Persistence

**Session 1:**
```
User: "My name is Alex"
Isabella: "Hey Alex! Nice to meet you! 💅"
```

**Session 2 (Same session_id):**
```
User: "What's my name?"
Isabella: "It's Alex, bestie! I don't forget my people! 😘"
```

### Example 3: Context-Aware Responses

```
User: "I'm working on a Python project"
Isabella: "Ooh Python! Love that for you! 🐍 What are you building?"

User: "Having trouble with async functions"
Isabella: "Async can be tricky! Let me help you out with that Python code..."
        ↑ (Remembers we're talking about Python from earlier)
```

---

## Troubleshooting

### Issue: Letta Not Initializing

**Symptom:**
```
⚠️ Letta library not installed (excluded due to security vulnerabilities)
Isabella will work without personality processing
```

**Solutions:**

1. **Check Installation:**
   ```bash
   pip list | grep letta
   ```

2. **Install Letta (if needed):**
   ```bash
   pip install letta
   ```

3. **Verify Import:**
   ```python
   from letta import create_client
   ```

### Issue: Personality Not Applied

**Symptom:** Responses lack personality/character

**Solutions:**

1. **Check Letta Status:**
   - Look for "✅ Letta personality engine ready!" in logs
   - If not present, Letta isn't active

2. **Verify Persona:**
   - Check `letta_service.py` persona definition
   - Ensure it's descriptive and specific

3. **Check LLM System Prompt:**
   - Edit `llm_service.py`
   - Add personality to system prompt as fallback

### Issue: Memory Not Persisting

**Symptom:** Agent forgets previous conversations

**Solutions:**

1. **Check Session ID:**
   - Ensure same `session_id` is used across requests
   - Frontend should maintain session ID

2. **Verify MongoDB:**
   - Check MongoDB connection
   - Verify messages are being saved

3. **Check Agent State:**
   - Agent may have been reset
   - Check logs for "Agent memory reset"

### Issue: Letta Errors in Production

**Symptom:** Errors or vulnerabilities in deployment

**Solution:**

**Disable Letta and use LLM prompts instead:**

1. Don't install Letta package
2. Update `llm_service.py` system prompt:
   ```python
   system_prompt = """You are Isabella - a sassy, confident AI assistant.
   [Full personality description here]"""
   ```
3. Use MongoDB for conversation history
4. Implement session-based context in application layer

---

## Advanced Topics

### Custom Agent Creation (Updated for Letta 0.16.x)

```python
from letta_client import Letta

client = Letta()

# Create memory blocks
memory_blocks = [
    {
        "label": "persona",
        "value": "Custom personality description",
        "template": False
    },
    {
        "label": "human",
        "value": "User description",
        "template": False
    }
]

# Create agent with new API
agent = client.agents.create(
    name="CustomAgent",
    memory_blocks=memory_blocks,
    system="Custom system instructions"
)
```

### Memory Management (Updated for Letta 0.16.x)

```python
# List agents
agents = client.agents.list(name="CustomAgent")

# Get specific agent
agent = client.agents.retrieve(agent_id=agent.id)

# Update agent (delete and recreate)
client.agents.delete(agent_id=agent.id)
# Then create new agent with updated settings

# Send message to agent
response = client.agents.messages.create(
    agent_id=agent.id,
    input="Your message here"
)
```

```python
# Update agent memory
client.update_agent_memory(
    agent_id=agent.id,
    memory_key="persona",
    memory_value="Updated personality"
)

# Clear memory
client.delete_agent(agent_id)
```

### Multi-Agent Systems (Updated for Letta 0.16.x)

```python
from letta_client import Letta

client = Letta()

# Create different agents for different purposes
support_memory = [
    {"label": "persona", "value": "Helpful support agent", "template": False},
    {"label": "human", "value": "User seeking help", "template": False}
]
creative_memory = [
    {"label": "persona", "value": "Creative and imaginative assistant", "template": False},
    {"label": "human", "value": "User seeking creative ideas", "template": False}
]

support_agent = client.agents.create(name="Support", memory_blocks=support_memory)
creative_agent = client.agents.create(name="Creative", memory_blocks=creative_memory)

# Route based on context
if user_needs_help:
    response = client.agents.messages.create(agent_id=support_agent.id, input=message)
else:
    response = client.agents.messages.create(agent_id=creative_agent.id, input=message)
```

---

## Summary

### Key Takeaways

1. **Letta is a personality & memory layer** - not a replacement for LLM
2. **Works alongside LLM system prompts** - complementary, not competitive  
3. **Provides stateful conversations** - remembers context across sessions
4. **Optional in LettaXRAG** - system works with or without it
5. **Security considerations** - current versions have vulnerabilities

### When to Use Letta

✅ **Use Letta when:**
- You need persistent personality across sessions
- You want complex memory management
- You're building conversational agents
- You need context-aware responses

❌ **Skip Letta when:**
- Simple Q&A system is sufficient
- Security is a primary concern
- You don't need session persistence
- Stateless interactions are acceptable

### Alternative Approaches

If not using Letta:

1. **LLM System Prompts**: Include personality in system prompt
2. **MongoDB History**: Store conversation history in database
3. **Application Layer**: Implement context management in code
4. **Session State**: Maintain state in application memory

---

## Resources

- **Letta Documentation**: https://docs.letta.ai
- **GitHub Repository**: https://github.com/letta-ai/letta
- **Security Advisory**: See project's SECURITY.md
- **Community Discord**: https://discord.gg/letta

---

**Last Updated**: January 2026 (Updated for Letta 0.16.x API)  
**Author**: LettaXRAG Team  
**Status**: Educational/Development Use Only
