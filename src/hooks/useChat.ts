import { useState, useCallback } from 'react';
import { chatAPI } from '../services/api';
import { useChatStore } from '../store/chatStore';
import type { Message } from '../types';

export const useChat = () => {
  const { messages, sessionId, isTyping, addMessage, setTyping } = useChatStore();
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content,
      sender: 'user',
      timestamp: new Date(),
    };
    addMessage(userMessage);

    // Set typing indicator
    setTyping(true);
    setError(null);

    try {
      // Call API
      const response = await chatAPI.sendMessage({
        message: content,
        session_id: sessionId,
      });

      // Add Isabella's response
      const isabellaMessage: Message = {
        id: crypto.randomUUID(),
        content: response.response,
        sender: 'isabella',
        timestamp: new Date(response.timestamp),
        ragSources: response.rag_sources,
      };
      addMessage(isabellaMessage);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
      
      // Add error message
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        content: 'Sorry babe, I\'m having trouble connecting right now. Please try again! 💅',
        sender: 'isabella',
        timestamp: new Date(),
      };
      addMessage(errorMessage);
    } finally {
      setTyping(false);
    }
  }, [sessionId, addMessage, setTyping]);

  return {
    messages,
    isTyping,
    error,
    sendMessage,
  };
};
