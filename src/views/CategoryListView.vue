<template>
  <div class="category-list-page">
    <div class="container">
      <h2 class="page-title">文章分类</h2>
      <p class="page-subtitle">{{ categories.length }} 个分类，探索不同主题</p>

      <div class="category-grid">
        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="`/category/${cat.slug}`"
          class="category-card"
        >
          <div class="card-bg"></div>
          <div class="card-inner">
            <div class="card-top">
              <h3 class="cat-name">{{ cat.name }}</h3>
              <span class="cat-count">{{ cat.articleCount }}</span>
            </div>
            <p v-if="cat.description" class="cat-desc">{{ cat.description }}</p>
            <p v-else class="cat-desc placeholder">暂无描述</p>
            <div class="card-arrow">
              <span>浏览文章</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </router-link>
      </div>

      <div v-if="categories.length === 0" class="empty-state">
        <el-empty description="暂无分类" :image-size="80" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import api from '../api'

useHead({
  title: '文章分类 - yuyudede',
  meta: [
    { name: 'description', content: '浏览所有文章分类' },
  ],
})

const categories = ref([])

async function fetchCategories() {
  const { data } = await api.get('/categories')
  categories.value = data
}

onMounted(fetchCategories)
</script>

<style scoped>
.category-list-page {
  padding: 48px 0 80px;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 32px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.category-card {
  position: relative;
  display: block;
  padding: 24px;
  border-radius: 18px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
  text-decoration: none;
  color: var(--text-primary);
  overflow: hidden;
  isolation: isolate;
  transition: transform 0.4s cubic-bezier(0.2,0.8,0.2,1),
              box-shadow 0.4s cubic-bezier(0.2,0.8,0.2,1),
              border-color 0.4s;
}

.card-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  background:
    radial-gradient(120% 80% at 100% 0%, rgba(139,92,246,0.12), transparent 62%),
    radial-gradient(120% 80% at 0% 100%, rgba(236,72,153,0.08), transparent 62%);
  opacity: 1;
  transition: opacity 0.4s;
  pointer-events: none;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 48px -12px rgba(15, 23, 42, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}
.category-card:hover .card-bg {
  opacity: 0;
}

.card-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.cat-name {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0;
}

.cat-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  background: rgba(129, 140, 248, 0.12);
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 600;
  flex-shrink: 0;
}

.cat-desc {
  color: var(--text-secondary);
  font-size: 0.88rem;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.cat-desc.placeholder {
  opacity: 0.5;
}

.card-arrow {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--primary);
  opacity: 0;
  transform: translateX(-6px);
  transition: all 0.3s;
}
.category-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

.empty-state {
  margin-top: 40px;
}
</style>
