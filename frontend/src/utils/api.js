import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({ baseURL: BASE_URL });

export const analyzeVideo = (formData, onUploadProgress) =>
  api.post('/analyze/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
    timeout: 120_000,
  });

export const fetchHistory = (sessionId) =>
  api.get(`/history/?session_id=${sessionId}`);

export const fetchAnalysis = (id) =>
  api.get(`/analysis/${id}/`);

export default api;
