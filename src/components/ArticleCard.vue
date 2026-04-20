<template>
  <el-card class="article-card" shadow="hover" @click="goToArticle">
    <template #header>
      <div class="card-header">
        <h3 class="card-title">{{ article.title }}</h3>
        <el-tag v-if="article.category" size="small" type="primary">
          {{ article.category.name || article.category }}
        </el-tag>
      </div>
    </template>
    <p class="card-summary">{{ article.summary }}</p>
    <div class="card-footer">
      <span class="card-date">{{ formatDate(article.createdAt) }}</span>
      <div class="card-tags">
        <el-tag
          v-for="tag in article.tagNames"
          :key="tag"
          size="small"
          type="info"
          effect="plain"
          class="tag-item"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function goToArticle() {
  router.push(`/article/${props.article.slug}`)
}
</script>

<style scoped>
.article-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-summary {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.card-date {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag-item {
  cursor: pointer;
}
</style>
