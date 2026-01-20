import { useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import { useChatStore } from '../store/chatStore';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import './ChatInterface.css';

const ChatInterface = () => {
  const { messages, isTyping, sendMessage } = useChat();
  const { clearMessages, isConnected } = useChatStore();
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
