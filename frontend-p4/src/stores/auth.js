import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export const useAuthStore = defineStore('auth', () => {
  const token = ref(sessionStorage.getItem('auth_token') || null)
  const username = ref(sessionStorage.getItem('auth_username') || null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(user, password) {
    const res = await fetch(`${API_BASE}/api/v1/token/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password })
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.non_field_errors?.[0] || 'Login failed')
    }

    const data = await res.json()
    token.value = data.auth_token
    username.value = user
    sessionStorage.setItem('auth_token', data.auth_token)
    sessionStorage.setItem('auth_username', user)
  }

  async function logout() {
    if (token.value) {
      try {
        await fetch(`${API_BASE}/api/v1/token/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token.value}`
          }
        })
      } catch (e) {
        // ignore network errors on logout
      }
    }
    token.value = null
    username.value = null
    sessionStorage.removeItem('auth_token')
    sessionStorage.removeItem('auth_username')
  }

  return { token, username, isAuthenticated, login, logout }
})
