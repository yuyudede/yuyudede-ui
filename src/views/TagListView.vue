<template>
  <div class="tag-list-page">
    <div class="container">
      <h2 class="page-title">标签云</h2>
      <div class="tag-cloud">
        <router-link
          v-for="tag in tags"
          :key="tag.id"
          :to="`/tag/${tag.slug}`"
          class="tag-link"
        >
          <el-tag
            size="large"
            effect="plain"
            round
            class="tag-item"
          >
            {{ tag.name }}
            <span class="tag-count">({{ tag.articleCount }})</span>
          </el-tag>
        </router-link>
      </div>
      <el-empty v-if="tags.length === 0" description="暂无标签" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const tags = ref([])

async function fetchTags() {
  const { data } = await api.get('/tags')
  tags.value = data
}

onMounted(fetchTags)
</script>

<style scoped>
.tag-list-page {
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

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-link {
  text-decoration: none;
}

.tag-item {
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}

.tag-item:hover {
  transform: scale(1.05);
  color: var(--primary);
  border-color: var(--primary);
}

.tag-count {
  margin-left: 4px;
  opacity: 0.7;
}
</style>
