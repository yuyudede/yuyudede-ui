<template>
  <section class="hero">
    <h1 class="hero-title">yuyudede's <span class="gradient-text">Blog</span></h1>
    <p class="subtitle">
      <span class="type-cursor">{{ displayText }}</span><span class="cursor">|</span>
    </p>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  stats: { type: Object, default: () => ({}) }
})

const fullText = '记录技术心得、源码笔记与生活碎片。'
const displayText = ref('')
let idx = 0
let timer = null

function type() {
  if (idx < fullText.length) {
    displayText.value = fullText.slice(0, idx + 1)
    idx++
    timer = setTimeout(type, 60 + Math.random() * 40)
  }
}

onMounted(() => {
  timer = setTimeout(type, 400)
})

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 72px 20px 48px;
}

.hero-title {
  font-size: clamp(2rem, 4.5vw, 3.2rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.15;
  margin-bottom: 12px;
  animation: fadeUp 0.6s both;
}

.gradient-text {
  background: linear-gradient(120deg, #8b5cf6, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  background-size: 200% 100%;
  animation: gradientFlow 4s ease infinite;
}

@keyframes gradientFlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.subtitle {
  font-size: clamp(0.92rem, 1.2vw, 1.05rem);
  color: var(--text-secondary);
  animation: fadeUp 0.6s 0.1s both;
  min-height: 1.6em;
}

.type-cursor {
  display: inline;
}

.cursor {
  display: inline-block;
  color: var(--primary);
  animation: blinkCursor 0.9s step-end infinite;
  margin-left: 1px;
}

@keyframes blinkCursor {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
