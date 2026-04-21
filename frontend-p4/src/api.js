import { useAuthStore } from './stores/auth'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export async function apiFetch(path, options = {}) {
  const auth = useAuthStore()

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  if (auth.token) {
    headers['Authorization'] = `Token ${auth.token}`
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  })

  return res
}
