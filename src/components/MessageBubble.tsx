import { useState } from 'react';
import type { Message } from '../types';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble = ({ message }: MessageBubbleProps) => {
  const [showSources, setShowSources] = useState(false);
  const isUser = message.sender === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'isabella'}`}>
      <div className="message-header">
        <span className="message-sender">
          {isUser ? '👤 You' : '✨ Isabella'}
        </span>
        <span className="message-time">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      <div className="message-content">{message.content}</div>
      {message.ragSources && message.ragSources.length > 0 && (
        <div className="message-sources">
          <button
            className="sources-toggle"
            onClick={() => setShowSources(!showSources)}
          >
            📚 {showSources ? 'Hide' : 'Show'} Sources ({message.ragSources.length})
          </button>
          {showSources && (
            <div className="sources-list">
              {message.ragSources.map((source, idx) => (
                <div key={idx} className="source-item">
                  📄 {source}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
