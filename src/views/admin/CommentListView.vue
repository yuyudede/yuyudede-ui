<template>
  <div class="comment-list-page">
    <h3>评论管理</h3>

    <el-table :data="comments" v-loading="loading" stripe>
      <el-table-column prop="articleTitle" label="文章" min-width="160" show-overflow-tooltip />
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="content" label="内容" min-width="200" show-overflow-tooltip />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.approved ? 'success' : 'warning'" size="small">
            {{ row.approved ? '已通过' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="!row.approved"
            size="small"
            type="success"
            @click="approveComment(row)"
          >
            通过
          </el-button>
          <el-popconfirm title="确定要删除这条评论吗？" @confirm="deleteComment(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../../api'

const comments = ref([])
const loading = ref(false)

async function fetchComments() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/comments')
    comments.value = data
  } finally {
    loading.value = false
  }
}

async function approveComment(comment) {
  try {
    const { data } = await api.put(`/admin/comments/${comment.id}/approve`)
    comment.approved = data.approved
    ElMessage.success('评论已通过')
  } catch {
    ElMessage.error('操作失败')
  }
}

async function deleteComment(id) {
  try {
    await api.delete(`/admin/comments/${id}`)
    ElMessage.success('删除成功')
    comments.value = comments.value.filter((c) => c.id !== id)
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchComments)
</script>

<style scoped>
.comment-list-page h3 {
  margin-bottom: 20px;
}
</style>
