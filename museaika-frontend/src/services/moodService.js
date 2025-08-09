import api from './api';

const moodService = {
  detectEmotionFromImage: async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await api.post('/detect/emotion', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  },

  analyzeSentiment: async (text) => {
    const response = await api.post('/detect/sentiment', { text });
    return response.data;
  },

  getMoodHistory: async () => {
    const response = await api.get('/detect/history');
    return response.data;
  }
};

export default moodService;