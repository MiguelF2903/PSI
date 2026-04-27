<template>
  <div class="audio-player">
    <audio
      ref="audioEl"
      id="my-audio"
      :src="src"
      @timeupdate="emitTimeUpdate"
      @ended="emitEnded"
    ></audio>

    <div class="audio-controls">
      <button class="btn btn-secondary" style="padding: 0.5rem 0.75rem" @click="togglePlay">
        {{ playing ? '⏸' : '▶' }}
      </button>
    </div>

    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPct + '%' }"></div>
    </div>

    <div class="time-label">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</div>
  </div>
</template>

<script setup>
import { ref, computed, defineExpose, onUnmounted } from 'vue'

const props = defineProps({
  src: { type: String, required: true }
})
const emit = defineEmits(['timeupdate', 'ended'])

const audioEl = ref(null)
const playing = ref(false)
const currentTime = ref(0)
const duration = ref(0)

const progressPct = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

function emitTimeUpdate() {
  if (!audioEl.value) return
  currentTime.value = audioEl.value.currentTime
  duration.value = audioEl.value.duration || 0
  emit('timeupdate', audioEl.value.currentTime)
}

function emitEnded() {
  playing.value = false
  emit('ended')
}

function togglePlay() {
  if (!audioEl.value) return
  if (audioEl.value.paused) {
    play()
  } else {
    pause()
  }
}

function play() {
  if (audioEl.value) {
    audioEl.value.play().catch(() => {})
    playing.value = true
    startTicker()
  }
}

function pause() {
  if (audioEl.value) {
    audioEl.value.pause()
    playing.value = false
    stopTicker()
  }
}

let ticker = null
function startTicker() {
  if (ticker) return
  ticker = setInterval(() => {
    emitTimeUpdate()
  }, 50) 
}

function stopTicker() {
  if (ticker) {
    clearInterval(ticker)
    ticker = null
  }
}

function formatTime(s) {
  if (!s || isNaN(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60).toString().padStart(2, '0')
  return `${m}:${sec}`
}


onUnmounted(stopTicker)

defineExpose({ play, pause })
</script>
