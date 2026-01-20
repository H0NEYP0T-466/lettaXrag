import { useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import { useChatStore } from './store/chatStore';
import { chatAPI } from './services/api';
import './App.css';

function App() {
  const { setConnected } = useChatStore();

  useEffect(() => {
    // Check backend health on mount and periodically
    const checkHealth = async () => {
      try {
        await chatAPI.getHealth();
        setConnected(true);
      } catch (error) {
        console.error('Health check failed:', error);
        setConnected(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s

    return () => clearInterval(interval);
  }, [setConnected]);

  return (
    <div className="app">
      <ChatInterface />
    </div>
  );
}

export default App;
