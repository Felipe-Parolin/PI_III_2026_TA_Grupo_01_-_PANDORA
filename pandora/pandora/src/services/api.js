// src/services/api.js

// Lê a URL base do arquivo .env (ou usa o localhost por padrão se o .env não existir)
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

// Função para pegar o token do localStorage e montar os Headers
const getHeaders = () => {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  };
  
  // Se o usuário estiver logado, envia o token de autorização
  if (token) {
    headers['Authorization'] = `Bearer ${token}`; // Mude para 'Token ${token}' se usar o token padrão do Django
  }
  
  return headers;
};

export const api = {
  // --- AUTENTICAÇÃO ---
  login: async (email, password) => {
    const response = await fetch(`${BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ 
        email: email, 
        senha: password 
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'E-mail ou senha incorretos.');
    }

    return response.json();
  },

  // --- CRUD GENÉRICO ---
  getAll: async (endpoint) => {
    const response = await fetch(`${BASE_URL}/${endpoint}/`, { 
      method: 'GET',
      headers: getHeaders() 
    });
    if (!response.ok) throw new Error(`Erro ao buscar ${endpoint}`);
    return response.json();
  },
  
  create: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}/${endpoint}/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`Erro ao criar em ${endpoint}`);
    return response.json();
  },

  update: async (endpoint, id, data) => {
    const response = await fetch(`${BASE_URL}/${endpoint}/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`Erro ao atualizar em ${endpoint}`);
    return response.json();
  },

  delete: async (endpoint, id) => {
    const response = await fetch(`${BASE_URL}/${endpoint}/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    if (!response.ok) throw new Error(`Erro ao deletar de ${endpoint}`);
    return true;
  }
};