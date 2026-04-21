<template>
  <div class="page animate-in">
    <div v-if="loading" class="spinner"></div>
    <div v-else-if="song" class="play-layout">
      <!-- Header with background info -->
      <div class="play-header">
        <img 
          v-if="song.background_image" 
          :src="resolveMediaUrl(song.background_image)" 
          class="play-cover" 
          alt="cover"
        />
        <div v-else class="play-cover" style="background: var(--bg-secondary); display:flex; align-items:center; justify-content:center;">🎵</div>
        
        <div class="play-meta">
          <h2>{{ song.title }}</h2>
          <p>{{ song.artist }}</p>
        </div>
      </div>

      <AudioPlayer
        ref="player"
        v-if="song"
        :src="resolveMediaUrl(song.audio_file)"
        @timeupdate="handleTimeUpdate"
        @ended="handleEnded"
      />

      <LyricsDisplay
        v-if="song"
        :song="song"
        :currentTime="currentTime"
        :songEnded="songEnded"
        @stopAudio="pauseAudio"
        @startAudio="resumeAudio"
        @summary="handleSummary"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { apiFetch } from '../api'
import { resolveMediaUrl } from '../utils'
import AudioPlayer from '../components/AudioPlayer.vue'
import LyricsDisplay from '../components/LyricsDisplay.vue'

const route = useRoute()
const auth = useAuthStore()
const song = ref(null)
const loading = ref(true)
const currentTime = ref(0)
const songEnded = ref(false)
const player = ref(null)

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await apiFetch(`/api/v1/songs/${id}/`)
    if (res.ok) {
      song.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to load song', e)
  } finally {
    loading.value = false
  }
})

function handleTimeUpdate(time) {
  currentTime.value = time
}

function handleEnded() {
  songEnded.value = true
}

function pauseAudio() {
  if (player.value) {
    player.value.pause()
  }
}

function resumeAudio() {
  if (player.value) {
    player.value.play()
  }
}

async function handleSummary({ correct, wrong }) {
  if (!auth.isAuthenticated) return
  try {
    await apiFetch('/api/v1/songusers/', {
      method: 'POST',
      body: JSON.stringify({
        song: song.value.id,
        correct_guesses: correct,
        wrong_guesses: wrong
      })
    })
  } catch (e) {
    console.error('Failed to save SongUser', e)
  }
}
</script>
