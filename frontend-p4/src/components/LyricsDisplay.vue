<template>
  <div class="lyrics-wrapper">
    <!-- Score board shown when song ends -->
    <div v-if="showSummary" class="score-board">
      <h2>🎉 Song Complete!</h2>
      <p class="score-text">Correct answers: <strong>{{ correctCount }}</strong> - Wrong answers: <strong>{{ wrongCount }}</strong></p>
      <RouterLink to="/" class="btn btn-primary">Back to Home</RouterLink>
    </div>

    <!-- Lyrics lines (3 at a time) -->
    <template v-else>
      <div
        v-for="(lineIdx, slot) in visibleSlots"
        :key="lineIdx"
        :class="['lyrics-line', slotClass(slot)]"
      >
        <template v-if="lineIdx >= 0 && lineIdx < parsedLines.length">
          <template v-for="(part, pi) in parsedLines[lineIdx].parts" :key="pi">
            <span v-if="part.type === 'text'">{{ part.text }}</span>
            <template v-else>
              <!-- Blank word -->
              <span v-if="part.revealed">
                <input
                  class="blank-input correct"
                  :value="part.word"
                  readonly
                />
              </span>
              <span v-else-if="slot === 1 && pi === activeBlankIndex">
                <!-- Active input for current blank -->
                <input
                  ref="activeInput"
                  class="blank-input"
                  :class="{ wrong: showWrong }"
                  data-cy="blankInput"
                  v-model="userInput"
                  type="text"
                  autocomplete="off"
                  spellcheck="false"
                  @keyup.enter="checkInput"
                />
              </span>
              <span v-else>
                <input
                  class="blank-input"
                  :style="{ width: Math.max(80, part.word.length * 12) + 'px' }"
                  placeholder="…"
                  readonly
                />
              </span>
            </template>
          </template>
        </template>
      </div>

      <!-- Controls -->
      <div style="display: flex; justify-content: center; margin-top: 1rem" v-if="!showSummary && hasActiveBlanks">
        <button class="btn btn-skip" data-cy="skip" @click="skipBlank">Skip</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { resolveMediaUrl } from '../utils'

const props = defineProps({
  song: { type: Object, required: true },
  currentTime: { type: Number, default: 0 },
  songEnded: { type: Boolean, default: false }
})

const emit = defineEmits(['stopAudio', 'startAudio', 'summary'])

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

/* ---------- LRC Parsing ---------- */
function parseLrc(text) {
  const lines = []
  for (const raw of text.split('\n')) {
    const line = raw.replace(/\r$/, '')
    // Match [mm:ss.xx] or [mm:ss:xx]
    const timeMatch = line.match(/^\[(\d+):(\d+)[.:](\d+)\](.*)/)
    if (!timeMatch) continue
    const minutes = parseInt(timeMatch[1])
    const seconds = parseInt(timeMatch[2])
    const centis = parseInt(timeMatch[3])
    const timestamp = minutes * 60 + seconds + centis / 100
    const lyric = timeMatch[4].trim()

    // parse parts: split on {word} tokens
    const parts = []
    const wordRe = /\{([^}]+)\}/g
    let last = 0
    let m
    while ((m = wordRe.exec(lyric)) !== null) {
      if (m.index > last) parts.push({ type: 'text', text: lyric.slice(last, m.index) })
      parts.push({ type: 'blank', word: m[1], revealed: false })
      last = m.index + m[0].length
    }
    if (last < lyric.length) parts.push({ type: 'text', text: lyric.slice(last) })

    lines.push({ timestamp, parts, lyric })
  }
  // sort by time
  lines.sort((a, b) => a.timestamp - b.timestamp)
  return lines
}

/* ---------- State ---------- */
const parsedLines = ref([])
const currentLineIndex = ref(0)
const activeBlankIndex = ref(-1)
const userInput = ref('')
const showWrong = ref(false)
const correctCount = ref(0)
const wrongCount = ref(0)
const showSummary = ref(false)
const activeInput = ref(null)

/* ---------- Computed ---------- */
// slots: [prevIndex, currentIndex, nextIndex]
const visibleSlots = computed(() => {
  const c = currentLineIndex.value
  return [c - 1, c, c + 1]
})

function slotClass(slot) {
  if (slot === 0) return 'is-prev'
  if (slot === 1) return 'is-current'
  return 'is-next'
}

const currentLine = computed(() => parsedLines.value[currentLineIndex.value] || null)

const hasActiveBlanks = computed(() => {
  if (!currentLine.value) return false
  return currentLine.value.parts.some((p) => p.type === 'blank' && !p.revealed)
})

/* ---------- Load LRC ---------- */
onMounted(async () => {
  if (!props.song?.lrc_file) return
  
  const url = resolveMediaUrl(props.song.lrc_file)
  try {
    const res = await fetch(url)
    const text = await res.text()
    parsedLines.value = parseLrc(text)
    findActiveBlank()
  } catch (e) {
    console.error('Failed to load LRC', e)
  }
})

/* ---------- Time sync ---------- */
function lineHasBlanks(idx) {
  const line = parsedLines.value[idx]
  if (!line) return false
  return line.parts.some(p => p.type === 'blank' && !p.revealed)
}

watch(() => props.currentTime, (time, oldTime) => {
  if (showSummary.value) return
  const lines = parsedLines.value
  if (!lines.length) return

  const syncOffset = 0.15
  let timeTargetIdx = 0
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].timestamp <= time + syncOffset) timeTargetIdx = i
    else break
  }

  // Detect movement
  const delta = time - (oldTime || 0)
  const isSeek = Math.abs(delta) > 0.25 // Clear jump
  const isForward = timeTargetIdx > currentLineIndex.value

  if (isForward) {
    // Only pause if it's natural playback and the CURRENT line still has blanks
    if (!isSeek && lineHasBlanks(currentLineIndex.value)) {
      emit('stopAudio')
      return 
    }
    // Advance and mark skipped as wrong
    for (let i = currentLineIndex.value; i < timeTargetIdx; i++) {
      for (const part of lines[i].parts) {
        if (part.type === 'blank' && !part.revealed) {
          part.revealed = true
          wrongCount.value++
        }
      }
    }
    currentLineIndex.value = timeTargetIdx
    findActiveBlank()
  } else if (timeTargetIdx < currentLineIndex.value) {
    // Backward movement: un-reveal if it's a seek
    if (isSeek) {
      for (let i = timeTargetIdx; i < lines.length; i++) {
        for (const part of lines[i].parts) {
          if (part.type === 'blank') part.revealed = false
        }
      }
    }
    currentLineIndex.value = timeTargetIdx
    findActiveBlank()
  }
})

/* ---------- Song ended ---------- */
watch(() => props.songEnded, (val) => {
  if (val) finishSong()
})

/* ---------- Helpers ---------- */
function findActiveBlank() {
  userInput.value = ''
  showWrong.value = false
  if (!currentLine.value) {
    activeBlankIndex.value = -1
    return
  }
  const idx = currentLine.value.parts.findIndex((p) => p.type === 'blank' && !p.revealed)
  activeBlankIndex.value = idx
  if (idx === -1) {
    // No blanks in this line — audio can continue freely
    emit('startAudio')
  }
  nextTick(() => {
    if (activeInput.value) {
      const el = Array.isArray(activeInput.value) ? activeInput.value[0] : activeInput.value
      if (el) el.focus()
    }
  })
}

function checkInput() {
  if (activeBlankIndex.value === -1) return
  const part = currentLine.value.parts[activeBlankIndex.value]
  if (!part) return

  const typed = userInput.value.trim().toLowerCase()
  const expected = part.word.toLowerCase()

  if (typed === expected) {
    // Correct!
    part.revealed = true
    correctCount.value++
    userInput.value = ''
    showWrong.value = false
    // Advance to next blank in line
    const nextBlankIdx = currentLine.value.parts.findIndex(
      (p, i) => p.type === 'blank' && !p.revealed && i > activeBlankIndex.value
    )
    if (nextBlankIdx === -1) {
      // No more blanks in this line — resume audio
      activeBlankIndex.value = -1
      emit('startAudio')
      checkIfFinished()
    } else {
      activeBlankIndex.value = nextBlankIdx
      nextTick(() => {
        const el = Array.isArray(activeInput.value) ? activeInput.value[0] : activeInput.value
        if (el) el.focus()
      })
    }
  } else {
    // Wrong
    wrongCount.value++
    showWrong.value = true
    userInput.value = ''
    // Pause audio
    emit('stopAudio')
    // Flash wrong state then reset
    setTimeout(() => { showWrong.value = false }, 400)
  }
}

function skipBlank() {
  if (activeBlankIndex.value === -1) return
  const part = currentLine.value.parts[activeBlankIndex.value]
  if (!part) return
  part.revealed = true
  wrongCount.value++
  userInput.value = ''
  showWrong.value = false

  const nextBlankIdx = currentLine.value.parts.findIndex(
    (p, i) => p.type === 'blank' && !p.revealed && i > activeBlankIndex.value
  )
  if (nextBlankIdx === -1) {
    activeBlankIndex.value = -1
    emit('startAudio')
    checkIfFinished()
  } else {
    activeBlankIndex.value = nextBlankIdx
    nextTick(() => {
      const el = Array.isArray(activeInput.value) ? activeInput.value[0] : activeInput.value
      if (el) el.focus()
    })
  }
}

function checkIfFinished() {
  const anyLeft = parsedLines.value.some(line => 
    line.parts.some(p => p.type === 'blank' && !p.revealed)
  )
  if (!anyLeft) {
    finishSong()
  }
}

function finishSong() {
  // Reveal any remaining blanks
  for (const line of parsedLines.value) {
    for (const part of line.parts) {
      if (part.type === 'blank' && !part.revealed) {
        part.revealed = true
        wrongCount.value++
      }
    }
  }
  showSummary.value = true
  emit('summary', { correct: correctCount.value, wrong: wrongCount.value })
}
</script>
