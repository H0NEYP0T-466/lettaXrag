import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Message } from '../types';

interface ChatState {
  messages: Message[];
  sessionId: string;
  isTyping: boolean;
  isDarkMode: boolean;
  isConnected: boolean;
  selectedModel: string;
  useRag: boolean;
  useLetta: boolean;
  addMessage: (message: Message) => void;
  setTyping: (typing: boolean) => void;
  toggleTheme: () => void;
  setConnected: (connected: boolean) => void;
  clearMessages: () => void;
  setSelectedModel: (model: string) => void;
  setUseRag: (useRag: boolean) => void;
  setUseLetta: (useLetta: boolean) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      messages: [],
      sessionId: crypto.randomUUID(),
      isTyping: false,
      isDarkMode: true,
      isConnected: false,
      selectedModel: 'longcat',
      useRag: true,
      useLetta: true,
      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),
      setTyping: (typing) => set({ isTyping: typing }),
      toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
      setConnected: (connected) => set({ isConnected: connected }),
      clearMessages: () => set({ messages: [] }),
      setSelectedModel: (model) => set({ selectedModel: model }),
      setUseRag: (useRag) => set({ useRag }),
      setUseLetta: (useLetta) => set({ useLetta }),
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        messages: state.messages,
        sessionId: state.sessionId,
        isDarkMode: state.isDarkMode,
        selectedModel: state.selectedModel,
        useRag: state.useRag,
        useLetta: state.useLetta,
      }),
      // Handle Date serialization/deserialization
      storage: {
        getItem: (name) => {
          const str = localStorage.getItem(name);
          if (!str) return null;
          const data = JSON.parse(str);
          // Convert timestamp strings back to Date objects
          if (data.state?.messages) {
            data.state.messages = data.state.messages.map((msg: Message) => ({
              ...msg,
              timestamp: new Date(msg.timestamp),
            }));
          }
          return data;
        },
        setItem: (name, value) => {
          localStorage.setItem(name, JSON.stringify(value));
        },
        removeItem: (name) => {
          localStorage.removeItem(name);
        },
      },
    }
  )
);
