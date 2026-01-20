import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Message } from '../types';

interface ChatState {
  messages: Message[];
  sessionId: string;
  isTyping: boolean;
  isDarkMode: boolean;
  isConnected: boolean;
  addMessage: (message: Message) => void;
  setTyping: (typing: boolean) => void;
  toggleTheme: () => void;
  setConnected: (connected: boolean) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      messages: [],
      sessionId: crypto.randomUUID(),
      isTyping: false,
      isDarkMode: true,
      isConnected: false,
      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),
      setTyping: (typing) => set({ isTyping: typing }),
      toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
      setConnected: (connected) => set({ isConnected: connected }),
      clearMessages: () => set({ messages: [] }),
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        messages: state.messages,
        sessionId: state.sessionId,
        isDarkMode: state.isDarkMode,
      }),
    }
  )
);
