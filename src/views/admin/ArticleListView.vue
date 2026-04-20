<template>
  <div class="article-list-page">
    <div class="toolbar">
      <h3>文章管理</h3>
      <el-button type="primary" @click="$router.push('/admin/articles/new')">
        新建文章
      </el-button>
    </div>

    <el-table :data="articles" v-loading="loading" stripe>
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
      <el-table-column label="分类" width="120">
        <template #default="{ row }">
          {{ row.category?.name || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.published ? 'success' : 'info'" size="small">
            {{ row.published ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.createdAt) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/admin/articles/edit/${row.id}`)">
            编辑
          </el-button>
          <el-button
            size="small"
            :type="row.published ? 'warning' : 'success'"
            @click="togglePublish(row)"
          >
            {{ row.published ? '取消发布' : '发布' }}
          </el-button>
          <el-popconfirm title="确定要删除这篇文章吗？" @confirm="deleteArticle(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

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
import { ElMessage } from 'element-plus'
import api from '../../api'

const articles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get('/admin/articles', { params: { page } })
    articles.value = data.content
    totalPages.value = data.totalPages
    totalElements.value = data.totalElements
    pageSize.value = data.size
  } finally {
    loading.value = false
  }
}

async function togglePublish(article) {
  try {
    const { data } = await api.put(`/admin/articles/${article.id}/toggle`)
    article.published = data.published
    ElMessage.success(data.published ? '已发布' : '已取消发布')
  } catch {
    ElMessage.error('操作失败')
  }
}

async function deleteArticle(id) {
  try {
    await api.delete(`/admin/articles/${id}`)
    ElMessage.success('删除成功')
    fetchArticles(currentPage.value - 1)
  } catch {
    ElMessage.error('删除失败')
  }
}

function handlePageChange(page) {
  currentPage.value = page
  fetchArticles(page - 1)
}

onMounted(() => fetchArticles())
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.toolbar h3 {
  margin: 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
