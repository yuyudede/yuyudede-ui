<template>
  <section class="hero">
    <h1 class="hero-title">yuyudede's <span class="gradient-text">Blog</span></h1>
    <p class="subtitle">记录技术心得、源码笔记与生活碎片。</p>
  </section>
</template>

<script setup>
defineProps({
  stats: { type: Object, default: () => ({}) }
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
}

.subtitle {
  font-size: clamp(0.92rem, 1.2vw, 1.05rem);
  color: var(--text-secondary);
  animation: fadeUp 0.6s 0.1s both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
