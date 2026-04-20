<template>
  <div class="category-list-page">
    <div class="container">
      <h2 class="page-title">文章分类</h2>
      <el-row :gutter="20">
        <el-col
          v-for="cat in categories"
          :key="cat.id"
          :xs="12"
          :sm="8"
          :md="6"
        >
          <el-card
            class="category-card"
            shadow="hover"
            @click="$router.push(`/category/${cat.slug}`)"
          >
            <h3 class="cat-name">{{ cat.name }}</h3>
            <p class="cat-desc" v-if="cat.description">{{ cat.description }}</p>
            <el-tag type="info" round size="small">{{ cat.articleCount }} 篇文章</el-tag>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-if="categories.length === 0" description="暂无分类" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const categories = ref([])

async function fetchCategories() {
  const { data } = await api.get('/categories')
  categories.value = data
}

onMounted(fetchCategories)
</script>

<style scoped>
.category-list-page {
  padding: 32px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 24px;
}

.category-card {
  cursor: pointer;
  margin-bottom: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.category-card:hover {
  transform: translateY(-4px);
}

.cat-name {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

.cat-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 12px;
}
</style>
