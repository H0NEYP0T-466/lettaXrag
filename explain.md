# LettaXRAG — Workflow Explanation

## What Does Letta Do?

Letta is **not** the final response generator on its own. It is a **context/memory engine**. Here is what it does:

1. **Persistent Memory** — Letta maintains an agent ("Isabella") with memory blocks (persona + human details). Every message you send is processed through this agent, and it remembers past conversations.
2. **Context Generation** — When you send a message, Letta processes it through the agent's memory and generates a **memory-aware context response**. This response is informed by all previous conversations and the agent's personality.
3. **Not a Standalone LLM** — For the `longcat` model specifically, Letta's response IS used as the final output because Letta internally calls the longcat LLM through its agent. For all other providers (Cerebras, Groq, Mistral), Letta generates context that is then **injected as a system message** into the actual LLM call.

## Full Message Flow

Here is exactly what happens when a user sends a message:

```
User sends message
        │
        ▼
┌─────────────────────────┐
│   Frontend (React)      │
│   - Adds user message   │
│     to chat display     │
│   - Sends POST /api/chat│
│     with: message,      │
│     model, use_rag,     │
│     use_letta           │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────────────────────────┐
│   Backend /api/chat route                   │
│                                             │
│   Step 1: RAG Retrieval (if use_rag=true)   │
│   - Embed user query with SentenceTransformer│
│   - FAISS similarity search (top 3 chunks)  │
│   - Returns relevant document excerpts      │
│                                             │
│   Step 2: LLM Service                       │
│   ┌─────────────────────────────────────┐   │
│   │ a) Letta Memory (if use_letta=true) │   │
│   │    - Send message + RAG context to  │   │
│   │      Letta agent (always uses       │   │
│   │      longcat model internally)      │   │
│   │    - Letta returns memory-aware     │   │
│   │      context response               │   │
│   │                                     │   │
│   │ b) If model=longcat AND Letta ok:   │   │
│   │    → Return Letta response directly │   │
│   │                                     │   │
│   │ c) If model=other (or Letta off):   │   │
│   │    - Build messages array:          │   │
│   │      • System instruction           │   │
│   │      • Letta context (if available) │   │
│   │      • RAG context (if available)   │   │
│   │      • User message                 │   │
│   │    - Call actual provider API        │   │
│   │      (Cerebras/Groq/Mistral)        │   │
│   │    → Return provider response       │   │
│   └─────────────────────────────────────┘   │
│                                             │
│   Step 3: Save to history.txt + MongoDB     │
│   Step 4: Return response + RAG sources     │
└───────────┬─────────────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│   Frontend              │
│   - Display response    │
│   - Show RAG sources    │
│     (collapsible)       │
└─────────────────────────┘
```

## What Gets Appended to the Prompt?

The final prompt sent to the LLM (for non-longcat models) is built like this:

| # | Role     | Content                                        |
|---|----------|------------------------------------------------|
| 1 | system   | Base system instruction (Isabella personality)  |
| 2 | system   | Letta memory context (if use_letta is enabled)  |
| 3 | system   | RAG retrieval results (if use_rag is enabled)   |
| 4 | user     | The actual user message (with timestamp prefix) |

For the **longcat** model with Letta enabled: Letta processes the message through its own agent (which already has the persona, memory, and receives the RAG context), so the Letta response is the final output — no separate LLM call is needed.

## Toggle Buttons

### Use RAG (default: ON)
- **ON**: The system retrieves relevant document chunks from FAISS and includes them in the prompt.
- **OFF**: RAG retrieval is skipped entirely. The LLM responds based only on its training data, Letta memory, and the user message.

### Use Letta (default: ON)
- **ON**: The Letta memory agent processes the message first, providing persistent conversation memory and personality context.
- **OFF**: Letta is bypassed. The LLM receives only the system instruction, RAG context (if enabled), and user message. No persistent memory across conversations.

## Why Letta Only Uses Longcat Internally

The Letta server manages its own agent with a specific LLM model. Previously, trying to use Cerebras/Groq/Mistral as the Letta agent's model caused **401 authentication errors** because the Letta server's internal provider registration had issues with those API keys.

The solution: Letta always uses the **longcat** model for its agent internally (memory processing). For non-longcat models, the Letta output is injected as context into the actual provider's API call. This way all models benefit from Letta's memory without needing their own Letta agents.
