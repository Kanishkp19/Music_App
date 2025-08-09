import api from './api';

const musicService = {
  getRecommendations: async (mood, limit = 20) => {
    const response = await api.get('/recommendations', {
      params: { mood, limit }
    });
    return response.data;
  },

  getPlaylists: async () => {
    const response = await api.get('/playlists');
    return response.data;
  },

  createPlaylist: async (title, tracks = []) => {
    const response = await api.post('/playlists', { title, tracks });
    return response.data;
  },

  generateMusic: async (mood, tempo = 120, length = 30) => {
    const response = await api.post('/generate', { mood, tempo, length });
    return response.data;
  },

  getGenerationStatus: async (jobId) => {
    const response = await api.get(`/generate/${jobId}`);
    return response.data;
  }
};

export default musicService;