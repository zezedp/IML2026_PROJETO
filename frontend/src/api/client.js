const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const makeUrl = (endpoint) => `${BASE_URL}${endpoint}`;

async function parseResponse(response) {
  if (!response.ok) {
    let detail = `API Error: ${response.status}`;
    try {
      const payload = await response.json();
      detail = payload.detail || detail;
    } catch {
      // Keep the generic message when the API does not return JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

export async function apiGet(endpoint) {
  const response = await fetch(makeUrl(endpoint));
  return parseResponse(response);
}

export async function apiPost(endpoint, body) {
  const response = await fetch(makeUrl(endpoint), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return parseResponse(response);
}
