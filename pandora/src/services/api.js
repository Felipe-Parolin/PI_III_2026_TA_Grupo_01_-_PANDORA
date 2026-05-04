import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await axios.post(`${BASE_URL}/authentication/token/refresh/`, {
            refresh: refreshToken
          });

          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
    }
    return Promise.reject(error);
  }
);

export const api = {
  login: async (email, password) => {
    try {
      const response = await apiClient.post('/authentication/token/', {
        email,
        password
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Usuário ou senha incorretos.');
    }
  },

  getAll: async (endpoint) => {
    const response = await apiClient.get(`/api/${endpoint}/`);
    return response.data;
  },

  create: async (endpoint, data) => {
    const response = await apiClient.post(`/api/${endpoint}/`, data);
    return response.data;
  },

  update: async (endpoint, id, data) => {
    const response = await apiClient.put(`/api/${endpoint}/${id}/`, data);
    return response.data;
  },

  delete: async (endpoint, id) => {
    const response = await apiClient.delete(`/api/${endpoint}/${id}/`);
    return response.data;
  }
};