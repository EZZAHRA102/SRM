import axios from 'axios';
import { ChatRequest, ChatResponse, OCRResult, HealthCheckResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const srmApi = {
  healthCheck: async (): Promise<HealthCheckResponse> => {
    const response = await api.get('/health');
    return response.data;
  },

  chat: async (payload: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat', payload);
    return response.data;
  },

  extractCil: async (file: File): Promise<OCRResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/ocr/extract-cil', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  extractBillInfo: async (file: File): Promise<OCRResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/ocr/extract-bill', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

