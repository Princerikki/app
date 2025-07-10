import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Get token from localStorage
const getToken = () => localStorage.getItem('token');

// Create axios instance with default headers
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  signup: async (userData) => {
    const response = await apiClient.post('/auth/signup', userData);
    return response.data;
  },
  
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },
  
  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
};

export const userAPI = {
  updateProfile: async (updateData) => {
    const response = await apiClient.put('/users/profile', updateData);
    return response.data;
  },
  
  getDiscoverUsers: async () => {
    const response = await apiClient.get('/users/discover');
    return response.data;
  },
  
  getUserProfile: async (userId) => {
    const response = await apiClient.get(`/users/profile/${userId}`);
    return response.data;
  },
};

export const swipeAPI = {
  swipeUser: async (swipeData) => {
    const response = await apiClient.post('/swipes/swipe', swipeData);
    return response.data;
  },
};

export const matchAPI = {
  getMatches: async () => {
    const response = await apiClient.get('/matches/');
    return response.data;
  },
};

export const messageAPI = {
  sendMessage: async (messageData) => {
    const response = await apiClient.post('/messages/send', messageData);
    return response.data;
  },
  
  getMessages: async (matchId) => {
    const response = await apiClient.get(`/messages/${matchId}`);
    return response.data;
  },
};

export default apiClient;