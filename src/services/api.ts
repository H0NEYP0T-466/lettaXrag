import axios from 'axios';
import type { ChatRequest, ChatResponse, HealthResponse, StatsResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat', request);
    return response.data;
  },

  getHealth: async (): Promise<HealthResponse> => {
    const response = await api.get<HealthResponse>('/api/health');
    return response.data;
  },

  getStats: async (): Promise<StatsResponse> => {
    const response = await api.get<StatsResponse>('/api/stats');
    return response.data;
  },

  uploadFile: async (file: File): Promise<{ message: string; filename: string; status: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
