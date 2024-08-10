import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/';

const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  get: <T>(url: string) => axiosInstance.get<T>(url).then((res) => res.data),
  post: <T>(url: string, data: any) => axiosInstance.post<T>(url, data).then((res) => res.data),
  put: <T>(url: string, data: any) => axiosInstance.put<T>(url, data).then((res) => res.data),
  delete: <T>(url: string) => axiosInstance.delete<T>(url).then((res) => res.data),
};