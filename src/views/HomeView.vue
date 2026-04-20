<template>
  <div class="home">
    <HeroSection />
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="16">
          <div v-loading="loading" class="article-list">
            <ArticleCard
              v-for="article in articles"
              :key="article.id"
              :article="article"
            />
            <el-empty v-if="!loading && articles.length === 0" description="暂无文章" />
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
        </el-col>
        <el-col :span="8">
          <el-card class="sidebar-card" shadow="never">
            <template #header>
              <span class="sidebar-title">分类</span>
            </template>
            <div class="category-list">
              <router-link
                v-for="cat in categories"
                :key="cat.id"
                :to="`/category/${cat.slug}`"
                class="category-item"
              >
                <span>{{ cat.name }}</span>
                <el-tag size="small" type="info" round>{{ cat.articleCount }}</el-tag>
              </router-link>
              <el-empty v-if="categories.length === 0" description="暂无分类" :image-size="60" />
            </div>
          </el-card>
          <el-card class="sidebar-card" shadow="never" style="margin-top: 20px">
            <template #header>
              <span class="sidebar-title">标签云</span>
            </template>
            <div class="tag-cloud">
              <router-link
                v-for="tag in tags"
                :key="tag.id"
                :to="`/tag/${tag.slug}`"
                class="tag-link"
              >
                <el-tag effect="plain" round>
                  {{ tag.name }} ({{ tag.articleCount }})
                </el-tag>
              </router-link>
              <el-empty v-if="tags.length === 0" description="暂无标签" :image-size="60" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get('/articles', { params: { page } })
    articles.value = data.content
    totalPages.value = data.totalPages
    totalElements.value = data.totalElements
    pageSize.value = data.size
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
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
}

.article-list {
  min-height: 200px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.sidebar-card {
  border-radius: 8px;
}

.sidebar-title {
  font-weight: 600;
  font-size: 1rem;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: color 0.2s;
}

.category-item:last-child {
  border-bottom: none;
}

.category-item:hover {
  color: var(--primary);
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-link {
  text-decoration: none;
}

.tag-link:hover .el-tag {
  color: var(--primary);
  border-color: var(--primary);
}
</style>
