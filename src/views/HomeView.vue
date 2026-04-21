<template>
  <div class="home">
    <HeroSection :stats="heroStats" />

    <div class="container" id="articles">
      <!-- Section 标题 -->
      <div class="section-head reveal">
        <div class="section-label">
          <span class="laser"></span>
          <span>LATEST ARTICLES</span>
        </div>
        <h2 class="section-title">
          最新<span class="grad">文章</span>
        </h2>
      </div>

      <el-row :gutter="28">
        <el-col :span="16" :xs="24" :sm="24" :md="16">
          <div v-loading="loading" class="article-list reveal">
            <ArticleCard
              v-for="article in articles"
              :key="article.id"
              :article="article"
            />
            <el-empty v-if="!loading && articles.length === 0" description="暂无文章" />
          </div>
          <div class="pagination-wrapper reveal">
            <el-pagination
              v-if="totalPages > 1"
              background
              layout="prev, pager, next"
              :total="totalElements"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            />
          </div>
        </el-col>

        <el-col :span="8" :xs="24" :sm="24" :md="8">
          <aside class="sidebar">
            <!-- 关于我 -->
            <div class="glass-card profile-card reveal">
              <div class="profile-glow"></div>
              <div class="avatar-ring">
                <div class="avatar">
                  <span>Y</span>
                </div>
              </div>
              <h3 class="profile-name">yuyudede</h3>
              <p class="profile-bio">Full-Stack Developer · Life Explorer</p>
              <div class="profile-socials">
                <a href="#" class="social">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.21.09 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.31 3.5 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.82.58C20.57 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/>
                  </svg>
                </a>
                <a href="#" class="social">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.302 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                  </svg>
                </a>
                <a href="#" class="social">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                  </svg>
                </a>
              </div>
            </div>

            <!-- 分类 -->
            <div class="glass-card reveal">
              <div class="card-title-row">
                <span class="dot"></span>
                <span class="sidebar-title">CATEGORIES</span>
              </div>
              <div class="category-list">
                <router-link
                  v-for="(cat, i) in categories"
                  :key="cat.id"
                  :to="`/category/${cat.slug}`"
                  class="category-item"
                  :style="{ '--delay': i * 0.05 + 's' }"
                >
                  <span class="cat-idx">{{ String(i + 1).padStart(2, '0') }}</span>
                  <span class="cat-name">{{ cat.name }}</span>
                  <span class="cat-count">{{ cat.articleCount }}</span>
                </router-link>
                <el-empty v-if="categories.length === 0" description="暂无分类" :image-size="60" />
              </div>
            </div>

            <!-- 标签云 -->
            <div class="glass-card reveal">
              <div class="card-title-row">
                <span class="dot dot-pink"></span>
                <span class="sidebar-title">TAG CLOUD</span>
              </div>
              <div class="tag-cloud">
                <router-link
                  v-for="tag in tags"
                  :key="tag.id"
                  :to="`/tag/${tag.slug}`"
                  class="tag-link"
                  :style="{ fontSize: tagSize(tag.articleCount) + 'rem' }"
                >
                  #{{ tag.name }}
                </router-link>
                <el-empty v-if="tags.length === 0" description="暂无标签" :image-size="60" />
              </div>
            </div>
          </aside>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import api from '../api'
import HeroSection from '../components/HeroSection.vue'
import ArticleCard from '../components/ArticleCard.vue'

const articles = ref([])
const categories = ref([])
const tags = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

const heroStats = computed(() => ({
  articles: totalElements.value || 0,
  categories: categories.value.length,
  tags: tags.value.length,
  days: Math.max(1, Math.floor((Date.now() - new Date('2024-01-01').getTime()) / 86400000))
}))

let observer = null

function setupReveal() {
  const els = document.querySelectorAll('.reveal')
  observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('reveal-in')
        observer.unobserve(e.target)
      }
    })
  }, { threshold: 0.12 })
  els.forEach(el => observer.observe(el))
}

function tagSize(count) {
  const max = Math.max(...tags.value.map(t => t.articleCount || 1), 1)
  return 0.78 + (count / max) * 0.5
}

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get('/articles', { params: { page } })
    articles.value = data.content
    totalPages.value = data.totalPages
    totalElements.value = data.totalElements
    pageSize.value = data.size
    await nextTick()
    setupReveal()
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  const { data } = await api.get('/categories')
  categories.value = data
}

async function fetchTags() {
  const { data } = await api.get('/tags')
  tags.value = data
}

function handlePageChange(page) {
  currentPage.value = page
  fetchArticles(page - 1)
}

onMounted(() => {
  fetchArticles()
  fetchCategories()
  fetchTags()
  nextTick(setupReveal)
})

onBeforeUnmount(() => {
  observer && observer.disconnect()
})
</script>

<style scoped>
.home {
  position: relative;
}

.container {
  position: relative;
  max-width: 1240px;
  margin: 0 auto;
  padding: 60px 20px 80px;
}

/* Section head */
.section-head {
  margin-bottom: 36px;
}
.section-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 0.72rem;
  letter-spacing: 4px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}
.laser {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, #818cf8, #ec4899, #22d3ee);
  background-size: 200% 100%;
  border-radius: 1px;
  animation: laserFlow 2s linear infinite;
}
@keyframes laserFlow {
  0% { background-position: 0 0; }
  100% { background-position: 200% 0; }
}
.section-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.grad {
  background: linear-gradient(120deg, #818cf8, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.article-list { min-height: 200px; }
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 28px;
  padding: 16px 24px;
  border-radius: 16px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
}

/* Sidebar 玻璃卡片 */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 90px;
}

.glass-card {
  position: relative;
  padding: 22px;
  border-radius: 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
}
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(400px circle at 0% 0%, rgba(129,140,248,0.12), transparent 50%);
  pointer-events: none;
}

/* 个人卡片 */
.profile-card {
  text-align: center;
  padding-top: 28px;
}
.profile-glow {
  position: absolute;
  inset: -40% -40% auto auto;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(236,72,153,0.3), transparent 70%);
  filter: blur(40px);
  pointer-events: none;
}
.avatar-ring {
  width: 88px; height: 88px;
  margin: 0 auto 16px;
  border-radius: 50%;
  padding: 3px;
  background: conic-gradient(from 0deg, #818cf8, #ec4899, #fbbf24, #22d3ee, #818cf8);
  animation: spin 6s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.avatar {
  width: 100%; height: 100%;
  border-radius: 50%;
  background: var(--bg-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  background-image: linear-gradient(135deg, var(--bg-surface), var(--bg-surface-2));
}
.profile-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.profile-bio {
  font-size: 0.82rem;
  color: var(--text-secondary);
  letter-spacing: 1px;
  margin-bottom: 16px;
}
.profile-socials {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.social {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(129,140,248,0.08);
  color: var(--text-secondary);
  transition: all 0.25s;
}
.social:hover {
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(129,140,248,0.4);
}

/* 卡片标题 */
.card-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #818cf8;
  box-shadow: 0 0 10px #818cf8;
}
.dot-pink {
  background: #ec4899;
  box-shadow: 0 0 10px #ec4899;
}
.sidebar-title {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--text-primary);
}

/* 分类 */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.category-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 10px;
  margin: 0 -10px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.25s;
  animation: slideIn 0.4s var(--delay,0s) both;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-8px); }
  to { opacity: 1; transform: translateX(0); }
}
.category-item:hover {
  background: linear-gradient(90deg, rgba(129,140,248,0.1), transparent);
  transform: translateX(4px);
}
.cat-idx {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.5;
}
.cat-name {
  flex: 1;
  font-size: 0.95rem;
}
.cat-count {
  font-size: 0.75rem;
  color: var(--text-secondary);
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(129,140,248,0.1);
}

/* 标签云 */
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: baseline;
}
.tag-link {
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.25s;
  line-height: 1.6;
}
.tag-link:hover {
  color: transparent;
  background: linear-gradient(120deg, #818cf8, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  transform: translateY(-2px);
}

/* Reveal —— 只做淡入+轻微模糊，避免位移 */
.reveal {
  opacity: 0;
  filter: blur(6px);
  transition: opacity 0.9s ease, filter 0.9s ease;
  will-change: opacity, filter;
}
.reveal-in {
  opacity: 1;
  filter: blur(0);
}

@media (max-width: 992px) {
  .sidebar { position: static; margin-top: 24px; }
}
</style>
