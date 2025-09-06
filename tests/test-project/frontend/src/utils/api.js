const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export async function fetchLorem(type = 'paragraph') {
  const response = await fetch(`${API_BASE}/api/${type}`);
  if (!response.ok) {
    throw new Error('Failed to fetch lorem text');
  }
  const data = await response.json();
  return data[type];
}
