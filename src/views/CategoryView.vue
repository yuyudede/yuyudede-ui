<template>
  <div class="category-page">
    <div class="container">
      <div class="page-header">
        <router-link to="/categories" class="back-link">← 全部分类</router-link>
        <h2 class="page-title">
          <span class="cat-name">{{ categoryName || route.params.slug }}</span>
          <span v-if="categoryDesc" class="cat-desc">{{ categoryDesc }}</span>
        </h2>
        <span class="article-count">{{ totalElements }} 篇文章</span>
      </div>

      <div v-loading="loading" class="article-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
        <el-empty v-if="!loading && articles.length === 0" description="该分类下暂无文章" />
      </div>

      <div class="pagination-wrapper" v-if="totalPages > 1">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="totalElements"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import api from '../api'
import ArticleCard from '../components/ArticleCard.vue'

const route = useRoute()

const articles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)
const categoryName = ref('')
const categoryDesc = ref('')

useHead({
  title: () => `${categoryName.value || route.params.slug} - yuyudede`,
  meta: () => [
    { name: 'description', content: `${categoryName.value || route.params.slug} 分类下的文章` },
    { property: 'og:title', content: categoryName.value || route.params.slug },
  ],
})

async function fetchCategoryInfo() {
  try {
    const { data } = await api.get('/categories')
    const cat = data.find(c => c.slug === route.params.slug)
    if (cat) {
      categoryName.value = cat.name
      categoryDesc.value = cat.description || ''
    }
  } catch {
    // ignore
  }
}

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get(`/categories/${route.params.slug}/articles`, {
      params: { page },
    })
    articles.value = data.content
    totalPages.value = data.totalPages
    totalElements.value = data.totalElements
    pageSize.value = data.size
  } finally {
    loading.value = false
  }
}

function handlePageChange(page) {
  currentPage.value = page
  fetchArticles(page - 1)
}

watch(() => route.params.slug, () => {
  currentPage.value = 1
  categoryName.value = ''
  categoryDesc.value = ''
  fetchCategoryInfo()
  fetchArticles()
})

onMounted(() => {
  fetchCategoryInfo()
  fetchArticles()
})
</script>

<style scoped>
.category-page {
  padding: 32px 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  margin-bottom: 32px;
}

.back-link {
  display: inline-block;
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.2s;
}
.back-link:hover {
  color: var(--primary);
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cat-name {
  background: linear-gradient(120deg, #8b5cf6, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.cat-desc {
  font-size: 0.95rem;
  font-weight: 400;
  color: var(--text-secondary);
}

.article-count {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.article-list {
  min-height: 200px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}
</style>
