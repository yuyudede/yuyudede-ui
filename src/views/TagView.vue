<template>
  <div class="tag-page">
    <div class="container">
      <h2 class="page-title">标签: {{ route.params.slug }}</h2>
      <div v-loading="loading" class="article-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
        <el-empty v-if="!loading && articles.length === 0" description="该标签下暂无文章" />
      </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import ArticleCard from '../components/ArticleCard.vue'

const route = useRoute()
const articles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get(`/tags/${route.params.slug}/articles`, {
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
  fetchArticles()
})

onMounted(() => fetchArticles())
</script>

<style scoped>
.tag-page {
  padding: 32px 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 24px;
}

.article-list {
  min-height: 200px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
