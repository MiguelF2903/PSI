<template>
  <div class="page" style="max-width: 420px">
    <div class="hero">
      <h1>Welcome Back 👋</h1>
      <p>Sign in to track your progress and save your scores.</p>
    </div>

    <div class="card">
      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <div class="form-group">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          data-cy="username"
          type="text"
          placeholder="Enter your username"
          @keyup.enter="login"
          autocomplete="username"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          data-cy="password"
          type="password"
          placeholder="Enter your password"
          @keyup.enter="login"
          autocomplete="current-password"
        />
      </div>

      <button class="btn btn-primary" style="width:100%" :disabled="loading" @click="login">
        {{ loading ? 'Signing in…' : 'Sign In' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function login() {
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password.'
    return
  }
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
