<template>
  <div class="search-page">
    <section class="search-hero">
      <p class="eyebrow">Search</p>
      <h1>找文章</h1>
      <form class="search-box" @submit.prevent="submitSearch">
        <input v-model="keyword" type="search" placeholder="输入关键词、主题或代码片段" />
        <button type="submit" :disabled="loading || !keyword.trim()">搜索</button>
      </form>
    </section>

    <section class="result-wrap">
      <div class="result-head">
        <span v-if="searched">共 {{ totalElements }} 条结果</span>
        <span v-else>输入关键词开始搜索</span>
      </div>

      <div v-loading="loading" class="result-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
        <el-empty
          v-if="searched && !loading && articles.length === 0"
          description="没有找到匹配的文章"
        />
      </div>

      <div v-if="totalPages > 1" class="pagination-wrapper">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="totalElements"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useHead } from '@unhead/vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import ArticleCard from '../components/ArticleCard.vue'

useHead({
  title: '搜索 - yuyudede',
})

const route = useRoute()
const router = useRouter()
const keyword = ref(String(route.query.q || ''))
const articles = ref([])
const loading = ref(false)
const searched = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

async function fetchResults(page = 0) {
  const q = keyword.value.trim()
  if (!q) {
    articles.value = []
    searched.value = false
    totalPages.value = 0
    totalElements.value = 0
    return
  }

  loading.value = true
  searched.value = true
  try {
    const { data } = await api.get('/articles/search', { params: { q, page } })
    articles.value = data.content
    totalPages.value = data.totalPages
    totalElements.value = data.totalElements
    pageSize.value = data.size
  } finally {
    loading.value = false
  }
}

function submitSearch() {
  currentPage.value = 1
  router.push({ name: 'Search', query: { q: keyword.value.trim() } })
}

function handlePageChange(page) {
  currentPage.value = page
  fetchResults(page - 1)
}

watch(
  () => route.query.q,
  (q) => {
    keyword.value = String(q || '')
    currentPage.value = 1
    fetchResults()
  },
  { immediate: true }
)
</script>

<style scoped>
.search-page {
  max-width: 980px;
  margin: 0 auto;
  padding: 52px 20px 88px;
}

.search-hero {
  text-align: center;
  padding: 28px 0 36px;
}

.eyebrow {
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.search-hero h1 {
  font-size: clamp(2rem, 5vw, 3.1rem);
  margin-bottom: 22px;
  letter-spacing: -0.02em;
}

.search-box {
  max-width: 660px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  padding: 8px;
  border-radius: 18px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.search-box input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  color: var(--text-primary);
  padding: 12px 14px;
  font: inherit;
  outline: none;
}

.search-box button {
  border: none;
  border-radius: 12px;
  padding: 0 22px;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-weight: 700;
  cursor: pointer;
}

.search-box button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.result-head {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 16px;
}

.result-list {
  min-height: 180px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 28px;
}

@media (max-width: 640px) {
  .search-box {
    flex-direction: column;
  }
  .search-box button {
    height: 42px;
  }
}
</style>
