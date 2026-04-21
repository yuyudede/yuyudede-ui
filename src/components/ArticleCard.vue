<template>
  <article
    ref="cardEl"
    class="article-card"
    @click="goToArticle"
    @mousemove="onMove"
    @mouseleave="onLeave"
    :style="cardStyle"
  >
    <div class="card-glow" :style="glowStyle"></div>
    <div class="card-border"></div>

    <div class="card-inner">
      <div class="card-header">
        <h3 class="card-title">
          <span class="title-text">{{ article.title }}</span>
        </h3>
        <el-tag v-if="article.category" size="small" effect="dark" class="cat-tag">
          {{ article.category.name || article.category }}
        </el-tag>
      </div>

      <p class="card-summary">{{ article.summary }}</p>

      <div class="card-footer">
        <span class="card-date">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <path d="M16 2v4M8 2v4M3 10h18"/>
          </svg>
          {{ formatDate(article.createdAt) }}
        </span>
        <div class="card-tags">
          <el-tag
            v-for="tag in article.tagNames"
            :key="tag"
            size="small"
            effect="plain"
            class="tag-item"
          >
            #{{ tag }}
          </el-tag>
        </div>
      </div>

      <div class="read-more">
        <span>READ MORE</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  article: { type: Object, required: true }
})

const router = useRouter()
const cardEl = ref(null)
const state = reactive({ rx: 0, ry: 0, mx: 50, my: 50, hover: false })

function onMove(e) {
  const rect = cardEl.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  state.mx = (x / rect.width) * 100
  state.my = (y / rect.height) * 100
  state.ry = ((x / rect.width) - 0.5) * 10
  state.rx = -((y / rect.height) - 0.5) * 10
  state.hover = true
}

function onLeave() {
  state.rx = 0
  state.ry = 0
  state.hover = false
}

const cardStyle = computed(() => ({
  transform: `perspective(900px) rotateX(${state.rx}deg) rotateY(${state.ry}deg) translateZ(0)`
}))

const glowStyle = computed(() => ({
  background: `radial-gradient(circle at ${state.mx}% ${state.my}%, rgba(129,140,248,0.35), transparent 50%)`,
  opacity: state.hover ? 1 : 0
}))

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function goToArticle() {
  router.push(`/article/${props.article.slug}`)
}
</script>

<style scoped>
.article-card {
  position: relative;
  margin-bottom: 20px;
  cursor: pointer;
  border-radius: 16px;
  transform-style: preserve-3d;
  transition: transform 0.2s cubic-bezier(0.2,0.8,0.2,1);
  background: var(--bg-surface);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  isolation: isolate;
}

.article-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 16px;
  background: linear-gradient(120deg,
    rgba(129,140,248,0) 0%,
    rgba(129,140,248,0.6) 40%,
    rgba(236,72,153,0.6) 60%,
    rgba(34,211,238,0) 100%);
  background-size: 200% 200%;
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s;
  animation: borderFlow 4s linear infinite;
  pointer-events: none;
  z-index: 2;
}
.article-card:hover::before { opacity: 1; }
@keyframes borderFlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

.card-glow {
  position: absolute;
  inset: 0;
  transition: opacity 0.4s;
  pointer-events: none;
  z-index: 0;
}

.card-border {
  position: absolute;
  inset: 0;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  pointer-events: none;
  z-index: 1;
}

.card-inner {
  position: relative;
  z-index: 2;
  padding: 22px 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
  transform: translateZ(30px);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.4;
  flex: 1;
}

.title-text {
  background-image: linear-gradient(120deg, #818cf8, #ec4899);
  background-size: 0% 2px;
  background-repeat: no-repeat;
  background-position: 0 100%;
  transition: background-size 0.5s;
}
.article-card:hover .title-text {
  background-size: 100% 2px;
}

.cat-tag {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important;
  color: #fff !important;
  flex-shrink: 0;
}

.card-summary {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transform: translateZ(20px);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px dashed var(--border-soft);
  transform: translateZ(15px);
  flex-wrap: wrap;
  gap: 8px;
}

.card-date {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 0.82rem;
}

.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag-item {
  cursor: pointer;
  transition: all 0.2s;
}
.tag-item:hover {
  color: #8b5cf6 !important;
  border-color: #8b5cf6 !important;
}

.read-more {
  position: absolute;
  top: 22px;
  right: 24px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  letter-spacing: 2px;
  font-weight: 600;
  color: #8b5cf6;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s;
}
.article-card:hover .read-more {
  opacity: 1;
  transform: translateX(0);
}
</style>
