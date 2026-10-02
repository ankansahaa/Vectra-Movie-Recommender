const BASE = '/api'

async function getJSON(url) {
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`)
  }
  return res.json()
}

export function fetchSuggestions() {
  return getJSON(`${BASE}/suggestions`)
}

export function fetchTrending(limit = 24) {
  return getJSON(`${BASE}/trending?limit=${limit}`)
}

export function fetchSearch(query, limit = 30) {
  return getJSON(`${BASE}/search?q=${encodeURIComponent(query)}&limit=${limit}`)
}

export function fetchMovie(id) {
  return getJSON(`${BASE}/movie/${id}`)
}
