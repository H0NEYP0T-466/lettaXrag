import { useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import { useChatStore } from '../store/chatStore';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import FileUpload from './FileUpload';
import './ChatInterface.css';

const ChatInterface = () => {
  const { messages, isTyping, sendMessage } = useChat();
  const { clearMessages, isConnected, isDarkMode } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className={`chat-interface ${isDarkMode ? 'dark' : 'light'}`}>
      <div className="chat-header">
        <div className="header-left">
          <h1 className="chat-title">
            <span className="title-icon">✨</span>
            Isabella
            <span className="title-badge">RAG AI</span>
          </h1>
          <p className="chat-subtitle">Your sassy AI assistant with knowledge</p>
        </div>
        <div className="header-right">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            {isConnected ? 'Connected' : 'Disconnected'}
          </div>
          <FileUpload />
          <button
            className="clear-button"
            onClick={clearMessages}
            title="Clear chat history"
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>👋 Hey there!</h2>
            <p>I'm Isabella, your sassy AI assistant with some serious knowledge.</p>
            <p>Ask me anything and I'll search through my documents to help you out! 💅</p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isTyping && (
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
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
