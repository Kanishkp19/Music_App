import axios from 'axios';
import { API_BASE_URL } from '@/utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/api/v1/auth/register', data),
  login: (data) => api.post('/api/v1/auth/login', data),
  getCurrentUser: () => api.get('/api/v1/auth/me'),
};

// Emotion API
export const emotionAPI = {
  analyzeImage: (formData) =>
    api.post('/api/v1/emotion/analyze/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  analyzeText: (text) => api.post('/api/v1/emotion/analyze/text', { text }),
  manualEntry: (emotion) => api.post('/api/v1/emotion/manual', { emotion }),
  getHistory: (limit = 50) => api.get('/api/v1/emotion/history', { params: { limit } }),
  getCurrent: () => api.get('/api/v1/emotion/current'),
};

// Music API
export const musicAPI = {
  search: (params) => api.get('/api/v1/music/search', { params }),
  getTrending: (params) => api.get('/api/v1/music/trending', { params }),
  getTrack: (trackId) => api.get(`/api/v1/music/track/${trackId}`),
  getRecommendations: (limit = 20) => api.get('/api/v1/music/recommend', { params: { limit } }),
  getCustomRecommendations: (data) => api.post('/api/v1/music/recommend/custom', data),
};

// Generator API
export const generatorAPI = {
  startGeneration: (data) => api.post('/api/v1/generate', data),
  getGenerationStatus: (jobId) => api.get(`/api/v1/generate/${jobId}`),
  downloadGeneration: (jobId) => api.get(`/api/v1/generate/${jobId}/download`, { responseType: 'blob' }),
  getGenerationHistory: (limit = 20) => api.get('/api/v1/generate/history', { params: { limit } }),
};

export default api;
