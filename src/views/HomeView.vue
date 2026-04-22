<template>
  <div class="home">
    <HeroSection />

    <div class="container" id="articles">
      <el-row :gutter="28">
        <el-col :span="16" :xs="24" :sm="24" :md="16">
          <div v-loading="loading" class="article-list">
            <ArticleCard
              v-for="article in articles"
              :key="article.id"
              :article="article"
            />
            <el-empty v-if="!loading && articles.length === 0" description="暂无文章" />
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
        </el-col>

        <el-col :span="8" :xs="24" :sm="24" :md="8">
          <aside class="sidebar">
            <!-- 关于我 -->
            <div class="glass-card profile-card">
              <div class="avatar">
                <span>Y</span>
              </div>
              <h3 class="profile-name">yuyudede</h3>
              <p class="profile-bio">执业兽医 · 程序员 · 唯物主义战士</p>
              <div class="profile-socials">
                <a href="#" class="social">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.21.09 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.31 3.5 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.82.58C20.57 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/>
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
            <div class="glass-card">
              <h4 class="sidebar-title">Categories</h4>
              <div class="category-list">
                <router-link
                  v-for="cat in categories"
                  :key="cat.id"
                  :to="`/category/${cat.slug}`"
                  class="category-item"
                >
                  <span class="cat-name">{{ cat.name }}</span>
                  <span class="cat-count">{{ cat.articleCount }}</span>
                </router-link>
                <el-empty v-if="categories.length === 0" description="暂无分类" :image-size="60" />
              </div>
            </div>

            <!-- 标签云 -->
            <div class="glass-card">
              <h4 class="sidebar-title">Tags</h4>
              <div class="tag-cloud">
                <router-link
                  v-for="tag in tags"
                  :key="tag.id"
                  :to="`/tag/${tag.slug}`"
                  class="tag-link"
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
import { ref, onMounted, nextTick } from 'vue'
import { useHead } from '@unhead/vue'
import api from '../api'
import HeroSection from '../components/HeroSection.vue'
import ArticleCard from '../components/ArticleCard.vue'

useHead({
  title: '博客 - yuyudede',
  meta: [
    { name: 'description', content: 'yuyudede 的个人博客，记录技术与生活' },
    { property: 'og:title', content: 'yuyudede 博客' },
    { property: 'og:description', content: 'yuyudede 的个人博客' },
    { property: 'og:url', content: 'https://yuyudede.com/blog' },
  ],
})

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
.home {
  position: relative;
}

.container {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px 80px;
}

.article-list {
  min-height: 200px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 28px;
}

/* Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 84px;
}

.glass-card {
  padding: 20px;
  border-radius: 16px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
}

/* Profile */
.profile-card {
  text-align: center;
  padding-top: 24px;
}
.avatar {
  width: 64px; height: 64px;
  margin: 0 auto 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
}
.profile-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.profile-bio {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 14px;
}
.profile-socials {
  display: flex;
  justify-content: center;
  gap: 8px;
}
.social {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: color 0.2s;
}
.social:hover {
  color: #8b5cf6;
}

/* Sidebar title */
.sidebar-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

/* Categories */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 0.92rem;
  transition: color 0.2s;
}
.category-item:hover {
  color: #8b5cf6;
}
.cat-count {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Tags */
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.tag-link {
  text-decoration: none;
  font-size: 0.82rem;
  color: var(--text-secondary);
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}
.tag-link:hover {
  color: #8b5cf6;
  border-color: #8b5cf6;
}

@media (max-width: 992px) {
  .sidebar { position: static; margin-top: 24px; }
}
</style>
