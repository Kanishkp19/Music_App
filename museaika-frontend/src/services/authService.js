import api from './api';

const authService = {
  getSpotifyAuthUrl: async () => {
    const response = await api.get('/auth/spotify/login');
    return response.data.auth_url;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data.user;
  },

  logout: async () => {
    await api.post('/auth/logout');
    localStorage.removeItem('access_token');
  }
};

export default authService;
