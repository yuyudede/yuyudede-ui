<template>
  <div class="codex-page">
    <section class="codex-hero">
      <div class="hero-copy">
        <span class="eyebrow">Codex Daily</span>
        <h1>Codex 日更</h1>
        <p>把每日协作里真正成型的想法沉淀成主题文章。</p>
      </div>
      <div class="hero-meter">
        <span class="meter-value">{{ totalElements }}</span>
        <span class="meter-label">已归档日期</span>
      </div>
    </section>

    <section class="codex-feed" v-loading="loading">
      <el-empty
        v-if="!loading && days.length === 0"
        description="暂无已发布的 Codex 文章"
        :image-size="110"
      />

      <article v-for="day in days" :key="day.date" class="day-group">
        <div class="day-rail">
          <time :datetime="day.date">{{ formatDay(day.date) }}</time>
          <span>{{ day.articles.length }} 篇</span>
        </div>
        <div class="day-articles">
          <router-link
            v-for="article in day.articles"
            :key="article.id"
            class="codex-article"
            :to="`/article/${article.slug}`"
          >
            <div class="article-topline">
              <h2>{{ article.title }}</h2>
              <span>{{ formatDate(article.createdAt) }}</span>
            </div>
            <p v-if="article.summary">{{ article.summary }}</p>
            <div class="article-tags">
              <el-tag
                v-for="tag in article.tagNames"
                :key="tag"
                size="small"
                effect="plain"
              >
                {{ tag }}
              </el-tag>
            </div>
          </router-link>
        </div>
      </article>
    </section>

    <div class="pagination-wrapper">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { ElMessage } from 'element-plus'
import api from '../api'

useHead({
  title: 'Codex 日更 - yuyudede',
  meta: [
    { name: 'description', content: '从每日 Codex 协作中整理出的主题文章归档' },
    { property: 'og:title', content: 'Codex 日更 - yuyudede' },
    { property: 'og:description', content: '从每日 Codex 协作中整理出的主题文章归档' },
    { property: 'og:url', content: 'https://yuyudede.com/codex' },
  ],
})

const days = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

function formatDay(dateStr) {
  const date = new Date(`${dateStr}T00:00:00`)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

async function fetchDays(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get('/codex/days', { params: { page } })
    days.value = data.content || []
    totalPages.value = data.totalPages || 0
    totalElements.value = data.totalElements || 0
    pageSize.value = data.size || 10
  } catch (err) {
    console.error('Failed to fetch Codex days:', err)
    ElMessage.error('获取 Codex 归档失败')
  } finally {
    loading.value = false
  }
}

function handlePageChange(page) {
  currentPage.value = page
  fetchDays(page - 1)
}

onMounted(() => fetchDays())
</script>

<style scoped>
.codex-page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 48px 22px 80px;
}

.codex-hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 28px;
  padding: 28px 0 34px;
  border-bottom: 1px solid var(--border-color);
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 10px;
  color: #0891b2;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 0;
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1;
  color: var(--text-primary);
}

.hero-copy p {
  max-width: 560px;
  margin: 16px 0 0;
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.8;
}

.hero-meter {
  min-width: 136px;
  padding: 18px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-surface);
  box-shadow: var(--shadow-sm);
}

.meter-value {
  display: block;
  color: var(--text-primary);
  font-size: 2.1rem;
  font-weight: 800;
  line-height: 1;
}

.meter-label {
  display: block;
  margin-top: 8px;
  color: var(--text-secondary);
  font-size: 0.82rem;
}

.codex-feed {
  min-height: 280px;
  padding-top: 28px;
}

.day-group {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  gap: 26px;
  padding: 26px 0;
  border-bottom: 1px solid var(--border-soft);
}

.day-rail {
  position: sticky;
  top: 86px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 0.86rem;
}

.day-rail time {
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 700;
}

.day-articles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.codex-article {
  display: block;
  padding: 18px 20px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-surface);
  color: inherit;
  text-decoration: none;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.codex-article:hover {
  transform: translateY(-2px);
  border-color: rgba(8, 145, 178, 0.42);
  box-shadow: 0 14px 34px -24px rgba(8, 145, 178, 0.55);
}

.article-topline {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.article-topline h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.08rem;
  line-height: 1.45;
}

.article-topline span {
  flex-shrink: 0;
  color: var(--text-secondary);
  font-size: 0.78rem;
  line-height: 1.6;
}

.codex-article p {
  margin: 10px 0 0;
  color: var(--text-secondary);
  line-height: 1.75;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 28px;
}

@media (max-width: 768px) {
  .codex-page {
    padding: 30px 18px 64px;
  }

  .codex-hero {
    align-items: stretch;
    flex-direction: column;
  }

  .hero-meter {
    width: 100%;
  }

  .day-group {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .day-rail {
    position: static;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .article-topline {
    flex-direction: column;
    gap: 4px;
  }
}
</style>
