import { useState, type KeyboardEvent } from 'react';
import './InputBox.css';

interface InputBoxProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const InputBox = ({ onSend, disabled }: InputBoxProps) => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-box">
      <textarea
        className="input-textarea"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask Isabella anything..."
        disabled={disabled}
        rows={1}
      />
      <button
        className="send-button"
        onClick={handleSend}
        disabled={!message.trim() || disabled}
      >
        {disabled ? '...' : '➤'}
      </button>
    </div>
  );
};

export default InputBox;
