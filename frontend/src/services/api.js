import axios from 'axios';

const base = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api';
export const api = axios.create({ baseURL: base });

export async function getDashboard() {
  const { data } = await api.get('/dashboard');
  return data;
}

export async function getRecent(limit = 20) {
  const { data } = await api.get('/recent', { params: { limit } });
  return data;
}

export async function lookup(indicator) {
  const { data } = await api.post('/lookup', { indicator });
  return data;
}
