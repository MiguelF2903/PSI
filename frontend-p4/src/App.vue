<template>
  <div>
    <nav class="navbar">
      <RouterLink class="brand" to="/">🎵 SongProject</RouterLink>
      <nav>
        <RouterLink class="nav-link" to="/" data-cy="home-cypress-test">Home</RouterLink>
        <RouterLink class="nav-link" to="/faq">FAQ</RouterLink>
        <RouterLink class="nav-link" to="/log-in" data-cy="login-cypress-test" v-if="!auth.isAuthenticated">Login</RouterLink>
        <RouterLink class="nav-link" to="/log-out" v-if="auth.isAuthenticated">Logout</RouterLink>
        <span v-if="auth.isAuthenticated" class="nav-link" style="color: var(--accent-cyan)">{{ auth.username }}</span>
      </nav>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
const auth = useAuthStore()
</script>
