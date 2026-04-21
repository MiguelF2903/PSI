<template>
  <div class="page animate-in">
    <div class="hero">
      <h1>Learn Songs by Ear 🎵</h1>
      <p>Listen to songs and fill in the missing lyrics. Improve your listening skills while enjoying great music.</p>
    </div>

    <!-- Search -->
    <div class="card shadow-glow" style="margin-bottom: 2rem">
      <p class="section-title">Search <span>Songs</span></p>
      <div class="search-bar">
        <div class="form-group" style="flex:1; margin-bottom:0">
          <input
            v-model="searchQuery"
            data-cy="search_text"
            type="text"
            placeholder="Search by title…"
            @keyup.enter="search"
          />
        </div>
        <button class="btn btn-primary" data-cy="search_button" @click="search">Search</button>
        <button class="btn btn-secondary" @click="randomSong">Random song</button>
      </div>

      <div v-if="searchResults.length" style="margin-top: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem">
        <button
          v-for="song in searchResults"
          :key="song.id"
          class="song-item"
          :data-cy="song.title"
          @click="goToSong(song.id)"
        >
          <img 
            v-if="song.background_image" 
            :src="resolveMediaUrl(song.background_image)" 
            class="song-thumbnail" 
            alt="cover"
          />
          <div v-else class="song-thumbnail-placeholder">🎵</div>
          
          <div class="song-info">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-artist">{{ song.artist }}</div>
          </div>
          <span class="song-plays">▶ Play</span>
        </button>
      </div>
      <div v-if="searchDone && !searchResults.length" class="alert alert-info" style="margin-top: 1rem">No songs found</div>
    </div>

    <!-- Top 3 Songs -->
    <p class="section-title">🏆 Most <span>Popular</span></p>
    <div v-if="loading" class="spinner"></div>
    <div v-else style="display: flex; flex-direction: column; gap: 0.75rem">
      <button
        v-for="(song, i) in topSongs"
        :key="song.id"
        class="song-item"
        :data-cy="song.title"
        @click="goToSong(song.id)"
      >
        <div class="song-rank">{{ i + 1 }}</div>
        
        <img 
          v-if="song.background_image" 
          :src="resolveMediaUrl(song.background_image)" 
          class="song-thumbnail" 
          alt="cover"
        />
        <div v-else class="song-thumbnail-placeholder">🎵</div>

        <div class="song-info">
          <div class="song-title">{{ song.title }}</div>
          <div class="song-artist">{{ song.artist }}</div>
        </div>
        <div class="song-plays">{{ song.number_times_played }} plays</div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
import { resolveMediaUrl } from '../utils'

const router = useRouter()

const topSongs = ref([])
const loading = ref(true)
const searchQuery = ref('')
const searchResults = ref([])
const searchDone = ref(false)

onMounted(async () => {
  try {
    const res = await apiFetch('/api/v1/songs/top/?n=3')
    if (res.ok) topSongs.value = await res.json()
  } catch (e) {
    console.error('Failed to load top songs', e)
  } finally {
    loading.value = false
  }
})

async function search() {
  if (!searchQuery.value.trim()) return
  searchDone.value = false
  searchResults.value = []
  try {
    const res = await apiFetch(`/api/v1/songs/search/?title=${encodeURIComponent(searchQuery.value)}`)
    if (res.ok) {
      searchResults.value = await res.json()
    }
  } catch (e) {
    console.error('Search failed', e)
  } finally {
    searchDone.value = true
  }
}

async function randomSong() {
  try {
    const res = await apiFetch('/api/v1/songs/random/')
    if (res.ok) {
      const song = await res.json()
      router.push(`/songs/${song.id}`)
    }
  } catch (e) {
    console.error('Random song failed', e)
  }
}

function goToSong(id) {
  router.push(`/songs/${id}`)
}
</script>

<style scoped>
.song-thumbnail {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  object-fit: cover;
  border: 1px solid var(--border);
}
.song-thumbnail-placeholder {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}
.animate-in {
  animation: fadeIn 0.4s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
