<template>
  <article
    ref="cardEl"
    class="article-card"
    @click="goToArticle"
    @mousemove="onMove"
    @mouseleave="onLeave"
  >
    <div class="card-glow" :style="glowStyle"></div>

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
const state = reactive({ mx: 50, my: 50, hover: false })

function onMove(e) {
  const rect = cardEl.value.getBoundingClientRect()
  state.mx = ((e.clientX - rect.left) / rect.width) * 100
  state.my = ((e.clientY - rect.top) / rect.height) * 100
  state.hover = true
}

function onLeave() {
  state.hover = false
}

const glowStyle = computed(() => ({
  background: `radial-gradient(circle at ${state.mx}% ${state.my}%, rgba(129,140,248,0.18), transparent 50%)`,
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
  border-radius: 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
  isolation: isolate;
  transition: transform 0.35s cubic-bezier(0.2,0.8,0.2,1),
              box-shadow 0.35s cubic-bezier(0.2,0.8,0.2,1),
              border-color 0.35s;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 48px -12px rgba(79, 70, 229, 0.15);
  border-color: rgba(139, 92, 246, 0.25);
}

.card-glow {
  position: absolute;
  inset: 0;
  transition: opacity 0.4s;
  pointer-events: none;
  z-index: 0;
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
  transition: opacity 0.25s;
}
.article-card:hover .cat-tag {
  opacity: 0;
  pointer-events: none;
}

.card-summary {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px dashed var(--border-soft);
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
