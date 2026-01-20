import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import type { Message } from '../types';
import 'katex/dist/katex.min.css';
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
          {isUser ? '$ user' : '> isabella'}
        </span>
        <span className="message-time">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      <div className="message-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex]}
          components={{
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            code({ inline, className, children }: any) {
              const match = /language-(\w+)/.exec(className || '');
              const codeString = String(children).replace(/\n$/, '');
              
              return !inline && match ? (
                <SyntaxHighlighter
                  style={vscDarkPlus as { [key: string]: React.CSSProperties }}
                  language={match[1]}
                  PreTag="div"
                >
                  {codeString}
                </SyntaxHighlighter>
              ) : (
                <code className={className}>
                  {children}
                </code>
              );
            },
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            table({ children }: any) {
              return (
                <div className="table-wrapper">
                  <table>{children}</table>
                </div>
              );
            },
          }}
        >
          {message.content}
        </ReactMarkdown>
      </div>
      {message.ragSources && message.ragSources.length > 0 && (
        <div className="message-sources">
          <button
            className="sources-toggle"
            onClick={() => setShowSources(!showSources)}
          >
            [sources: {message.ragSources.length}] {showSources ? '[-]' : '[+]'}
          </button>
          {showSources && (
            <div className="sources-list">
              {message.ragSources.map((source, idx) => (
                <div key={idx} className="source-item">
                  → {source}
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
