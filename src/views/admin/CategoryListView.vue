<template>
  <div class="category-list-page">
    <div class="toolbar">
      <h3>分类管理</h3>
      <button class="btn-primary" @click="$router.push('/admin/categories/new')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        新建分类
      </button>
    </div>

    <div class="table-wrap glass-card" v-loading="loading">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>Slug</th>
            <th>描述</th>
            <th>文章数</th>
            <th class="col-actions">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td class="col-id">{{ cat.id }}</td>
            <td class="col-name">{{ cat.name }}</td>
            <td class="col-slug">{{ cat.slug }}</td>
            <td class="col-desc">{{ cat.description || '-' }}</td>
            <td class="col-count">
              <span class="count-badge">{{ cat.articleCount }}</span>
            </td>
            <td class="col-actions">
              <button class="btn-icon" @click="$router.push(`/admin/categories/edit/${cat.id}`)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button class="btn-icon danger" @click="confirmDelete(cat)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
              </button>
            </td>
          </tr>
          <tr v-if="categories.length === 0">
            <td colspan="6" class="col-empty">暂无分类</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 删除确认弹窗 -->
    <el-dialog v-model="dialogVisible" title="确认删除" width="360px" align-center>
      <p>确定要删除分类 <strong>{{ deleteTarget?.name }}</strong> 吗？</p>
      <p class="dialog-tip">该分类下的文章将变为未分类状态。</p>
      <template #footer>
        <button class="btn-secondary" @click="dialogVisible = false">取消</button>
        <button class="btn-danger" @click="handleDelete">删除</button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../../api'

const categories = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const deleteTarget = ref(null)

async function fetchCategories() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/categories')
    categories.value = data
  } finally {
    loading.value = false
  }
}

function confirmDelete(cat) {
  deleteTarget.value = cat
  dialogVisible.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  try {
    await api.delete(`/admin/categories/${deleteTarget.value.id}`)
    ElMessage.success('删除成功')
    dialogVisible.value = false
    fetchCategories()
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchCategories)
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
  font-size: 1.15rem;
  font-weight: 600;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 16px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(129, 140, 248, 0.5);
}

.btn-secondary {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.btn-danger {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: #ef4444;
  color: #fff;
  font-size: 0.85rem;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-danger:hover {
  opacity: 0.9;
}

.glass-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
  overflow: hidden;
}

.table-wrap {
  padding: 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.data-table th {
  text-align: left;
  padding: 14px 16px;
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.82rem;
  border-bottom: 1px solid var(--border-soft);
  background: rgba(129, 140, 248, 0.04);
}
.data-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-soft);
  color: var(--text-primary);
}
.data-table tr:hover td {
  background: rgba(129, 140, 248, 0.04);
}
.data-table tr:last-child td {
  border-bottom: none;
}

.col-id { width: 60px; color: var(--text-secondary); font-size: 0.82rem; }
.col-name { font-weight: 600; }
.col-slug { color: var(--text-secondary); font-size: 0.85rem; font-family: 'Fira Code', monospace; }
.col-desc { color: var(--text-secondary); max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.col-count { width: 80px; }
.col-actions { width: 100px; text-align: right; white-space: nowrap; }
.col-empty { text-align: center; color: var(--text-secondary); padding: 40px 0; }

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  background: rgba(129, 140, 248, 0.12);
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 600;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-icon:hover {
  background: rgba(129, 140, 248, 0.1);
  color: var(--primary);
}
.btn-icon.danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.dialog-tip {
  margin-top: 8px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}
</style>
