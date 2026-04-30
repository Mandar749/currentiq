const API_BASE = 'https://currentiq-backend.onrender.com';

export const getHeadlines = () =>
  fetch(`${API_BASE}/headlines`).then(r => r.json());

export const getDigest = (exam, days = 1, topic = null) =>
  fetch(`${API_BASE}/digest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ exam, days, topic })
  }).then(r => r.json());

export const getMCQs = (exam, topic, count = 5) =>
  fetch(`${API_BASE}/mcq`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ exam, topic, count })
  }).then(r => r.json());

export const evaluateAnswer = (question, answer, word_limit = 150) =>
  fetch(`${API_BASE}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, answer, word_limit })
  }).then(r => r.json());