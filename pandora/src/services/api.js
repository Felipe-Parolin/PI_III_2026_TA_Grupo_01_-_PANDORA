// src/services/api.js

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

const getHeaders = () => {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
};

const getErrorMessage = (errorData, fallbackMessage) => {
  const firstFieldError = Array.isArray(Object.values(errorData)[0])
    ? Object.values(errorData)[0][0]
    : undefined;

  return errorData.detail || errorData.message || firstFieldError || fallbackMessage;
};

const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) return null;

  const response = await fetch(`${BASE_URL}/token/refresh/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    },
    body: JSON.stringify({
      refresh: refreshToken
    })
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json().catch(() => ({}));
  const newAccessToken = data?.access || data?.access_token;

  if (newAccessToken) {
    localStorage.setItem('access_token', newAccessToken);
  }

  if (data?.refresh || data?.refresh_token) {
    localStorage.setItem('refresh_token', data.refresh || data.refresh_token);
  }

  return newAccessToken || null;
};

const authenticatedRequest = async (url, options = {}, fallbackMessage = 'Erro na requisicao.') => {
  let response = await fetch(url, {
    ...options,
    headers: getHeaders(),
  });

  if (response.status === 401) {
    const refreshedToken = await refreshAccessToken();

    if (refreshedToken) {
      response = await fetch(url, {
        ...options,
        headers: getHeaders(),
      });
    }
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(getErrorMessage(errorData, fallbackMessage));
  }

  return response;
};

export const api = {
  login: async (email, password) => {
    const response = await fetch(`${BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify({
        email,
        username: email,
        password
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(getErrorMessage(errorData, 'Usuário ou senha incorretos.'));
    }

    return response.json();
  },

  getAll: async (endpoint) => {
    const response = await authenticatedRequest(
      `${BASE_URL}/${endpoint}/`,
      { method: 'GET' },
      `Erro ao buscar ${endpoint}`
    );
    return response.json();
  },

  create: async (endpoint, data) => {
    const response = await authenticatedRequest(
      `${BASE_URL}/${endpoint}/`,
      {
        method: 'POST',
        body: JSON.stringify(data)
      },
      `Erro ao criar em ${endpoint}`
    );
    return response.json();
  },

  update: async (endpoint, id, data) => {
    const response = await authenticatedRequest(
      `${BASE_URL}/${endpoint}/${id}/`,
      {
        method: 'PUT',
        body: JSON.stringify(data)
      },
      `Erro ao atualizar em ${endpoint}`
    );
    return response.json();
  },

  delete: async (endpoint, id) => {
    const response = await authenticatedRequest(
      `${BASE_URL}/${endpoint}/${id}/`,
      { method: 'DELETE' },
      `Erro ao deletar de ${endpoint}`
    );
    return true;
  }
};
