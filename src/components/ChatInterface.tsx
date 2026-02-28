import { useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import { useChatStore } from '../store/chatStore';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import './ChatInterface.css';

const MODEL_OPTIONS = [
  { value: 'longcat', label: 'LongCat Flash Lite' },
  { value: 'cerebras', label: 'GPT-OSS 120B (Cerebras)' },
  { value: 'llama-4-maverick', label: 'Llama 4 Maverick 17B (Groq)' },
  { value: 'llama-4-scout', label: 'Llama 4 Scout 17B (Groq)' },
  { value: 'kimi-k2-instruct-0905', label: 'Kimi K2 Instruct 0905 (Groq)' },
  { value: 'kimi-k2-instruct', label: 'Kimi K2 Instruct (Groq)' },
  { value: 'mistral-large', label: 'Mistral Large 2411' },
];

const ChatInterface = () => {
  const { messages, isTyping, sendMessage } = useChat();
  const { clearMessages, isConnected, selectedModel, setSelectedModel, useRag, setUseRag, useLetta, setUseLetta } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-content">
          <span className="prompt-symbol">$ </span>
          <span className="header-title">lettaxrag</span>
          <select
            className="model-selector"
            value={selectedModel}
            onChange={(e) => {
              setSelectedModel(e.target.value);
              console.log("Model changed to:", e.target.value);
            }}
            title="Select base model"
          >
            {MODEL_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <label className="toggle-label" title="Enable/disable RAG retrieval">
            <input
              type="checkbox"
              checked={useRag}
              onChange={(e) => setUseRag(e.target.checked)}
            />
            <span className="toggle-text">RAG</span>
          </label>
          <label className="toggle-label" title="Enable/disable Letta memory">
            <input
              type="checkbox"
              checked={useLetta}
              onChange={(e) => setUseLetta(e.target.checked)}
            />
            <span className="toggle-text">Letta</span>
          </label>
          <span className="status-indicator">
            [{isConnected ? 'online' : 'offline'}]
          </span>
          <button className="clear-button" onClick={clearMessages} title="Clear chat">
            [clear]
          </button>
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <div>$ system: ready</div>
            <div>$ agent: isabella</div>
            <div>$ mode: rag-enhanced</div>
            <div>&nbsp;</div>
            <div>&gt; Type your message below...</div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isTyping && (
              <div className="typing-indicator">
                <span>&gt; processing...</span>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputBox onSend={sendMessage} disabled={isTyping} />
    </div>
  );
};

export default ChatInterface;
