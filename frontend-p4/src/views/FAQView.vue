<template>
  <div class="page animate-in">
    <div class="hero">
      <h1>F.A.Q. ❓</h1>
      <p>Answers to the most common questions about SongProject.</p>
    </div>

    <div class="faq-container">
      <div v-for="(item, i) in faqs" :key="i" class="card faq-item shadow-glow">
        <h3 class="faq-question">Q: {{ item.question }}</h3>
        <p class="faq-answer">A: {{ item.answer }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const faqs = [
  {
    question: "What is SongProject?",
    answer: "SongProject is a web application designed to help you improve your listening skills by filling in missing lyrics in your favorite songs."
  },
  {
    question: "How do I play?",
    answer: "Search for a song, click play, and listen! Type the missing words as you hear them. If you're stuck, use the 'Skip' button."
  },
  {
    question: "Do I need an account?",
    answer: "No, you can play as an anonymous user. However, if you create an account and log in, your progress and scores will be saved."
  },
  {
    question: "How is the score calculated?",
    answer: "You get points for each correct word. Each incorrect attempt or use of the skip button counts as an error."
  }
]
</script>

<style scoped>
.faq-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}
.faq-item {
  text-align: left;
}
.faq-question {
  color: var(--accent-cyan);
  font-family: 'Outfit', sans-serif;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}
.faq-answer {
  color: var(--text-secondary);
}
.animate-in {
  animation: fadeIn 0.4s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
