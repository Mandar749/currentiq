import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const api = axios.create({ baseURL: API_BASE });

export const getHeadlines = () => 
  api.get('/headlines').then(r => r.data);

export const getDigest = (exam, days = 1, topic = null) => 
  api.post('/digest', { exam, days, topic }).then(r => r.data);

export const getMCQs = (exam, topic, count = 5) => 
  api.post('/mcq', { exam, topic, count }).then(r => r.data);

export const evaluateAnswer = (question, answer, word_limit = 150) => 
  api.post('/evaluate', { question, answer, word_limit }).then(r => r.data);