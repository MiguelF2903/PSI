<template>
  <div class="page" style="max-width: 500px; text-align: center; padding-top: 4rem">
    <div class="card">
      <div style="font-size: 3rem; margin-bottom: 1rem">👋</div>
      <h1 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; margin-bottom: 0.5rem">You've been logged out</h1>
      <p style="color: var(--text-secondary); margin-bottom: 1.5rem">
        Your session has been ended successfully. Redirecting to home in
        <strong style="color: var(--accent-cyan)">{{ countdown }}</strong> seconds…
      </p>
      <RouterLink to="/" class="btn btn-primary">Go to Home Now</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const countdown = ref(5)

let interval

onMounted(async () => {
  await auth.logout()
  interval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(interval)
      router.push('/')
    }
  }, 1000)
})

onUnmounted(() => clearInterval(interval))
</script>
