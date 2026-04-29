<template>
  <div class="codex-admin-page">
    <div class="toolbar">
      <div>
        <h3>Codex 导入</h3>
        <p>本地任务生成的 Markdown 会进入文章草稿。</p>
      </div>
      <el-button :icon="Refresh" circle @click="fetchArticles" :loading="loading" />
    </div>

    <section class="import-panel">
      <div class="panel-heading">
        <div>
          <h4>上传目标</h4>
          <code>{{ endpoint }}</code>
        </div>
        <el-tag type="info" effect="plain">Bearer JWT</el-tag>
      </div>

      <el-input
        v-model="payloadText"
        type="textarea"
        :rows="13"
        spellcheck="false"
        class="payload-input"
      />

      <div class="import-actions">
        <el-button @click="resetPayload">恢复示例</el-button>
        <el-button type="primary" :loading="importing" @click="submitImport">
          导入草稿
        </el-button>
      </div>

      <div v-if="importResult" class="result-panel">
        <div class="result-stats">
          <span>创建 {{ importResult.created }}</span>
          <span>更新 {{ importResult.updated }}</span>
          <span>跳过 {{ importResult.skipped }}</span>
          <span>失败 {{ importResult.failed }}</span>
        </div>
        <el-table :data="importResult.items" stripe size="small">
          <el-table-column prop="title" label="标题" min-width="180" show-overflow-tooltip />
          <el-table-column prop="slug" label="Slug" min-width="180" show-overflow-tooltip />
          <el-table-column label="状态" width="150">
            <template #default="{ row }">
              <el-tag :type="statusType(row.status)" size="small">
                {{ statusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="结果" min-width="180" show-overflow-tooltip />
        </el-table>
      </div>
    </section>

    <section class="table-panel">
      <div class="panel-heading">
        <div>
          <h4>最近导入</h4>
          <p>发布操作继续在文章管理中完成。</p>
        </div>
      </div>

      <el-table :data="articles" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="220" show-overflow-tooltip />
        <el-table-column prop="sourceDate" label="来源日期" width="120" />
        <el-table-column prop="sourceExternalId" label="External ID" min-width="180" show-overflow-tooltip />
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.published ? 'success' : 'info'" size="small">
              {{ row.published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="120">
          <template #default="{ row }">
            {{ formatDate(row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/admin/articles/edit/${row.id}`)">
              编辑
            </el-button>
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
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import api from '../../api'

const endpoint = 'http://124.221.73.2/api/admin/codex/articles/import'
const samplePayload = {
  sourceDate: '2026-04-29',
  items: [
    {
      externalId: 'agent-memory-refactor',
      title: 'Agent 记忆系统重构思考',
      slug: 'agent-memory-refactor',
      summary: '从一次 Codex 对话中整理出的记忆系统设计要点。',
      content: '# Agent 记忆系统重构思考\n\n...',
      categoryName: 'Codex 日更',
      tagNames: ['codex', 'agent', '架构'],
    },
  ],
}

const payloadText = ref(JSON.stringify(samplePayload, null, 2))
const importResult = ref(null)
const importing = ref(false)
const loading = ref(false)
const articles = ref([])
const currentPage = ref(1)
const totalPages = ref(0)
const totalElements = ref(0)
const pageSize = ref(10)

function resetPayload() {
  payloadText.value = JSON.stringify(samplePayload, null, 2)
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function statusType(status) {
  if (status === 'CREATED') return 'success'
  if (status === 'UPDATED') return 'warning'
  if (status === 'SKIPPED_PUBLISHED') return 'info'
  return 'danger'
}

function statusLabel(status) {
  const labels = {
    CREATED: '已创建',
    UPDATED: '已更新',
    SKIPPED_PUBLISHED: '已发布跳过',
    FAILED: '失败',
  }
  return labels[status] || status
}

async function submitImport() {
  let payload
  try {
    payload = JSON.parse(payloadText.value)
  } catch {
    ElMessage.error('JSON 格式不正确')
    return
  }

  importing.value = true
  try {
    const { data } = await api.post('/admin/codex/articles/import', payload)
    importResult.value = data
    ElMessage.success('导入完成')
    fetchArticles(currentPage.value - 1)
  } catch (err) {
    console.error('Failed to import Codex articles:', err)
    ElMessage.error('导入失败: ' + (err.response?.data?.detail || err.response?.data?.message || err.message || '未知错误'))
  } finally {
    importing.value = false
  }
}

async function fetchArticles(page = 0) {
  loading.value = true
  try {
    const { data } = await api.get('/admin/codex/articles', { params: { page } })
    articles.value = data.content || []
    totalPages.value = data.totalPages || 0
    totalElements.value = data.totalElements || 0
    pageSize.value = data.size || 10
  } catch (err) {
    console.error('Failed to fetch Codex articles:', err)
    ElMessage.error('获取 Codex 文章失败')
  } finally {
    loading.value = false
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
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.toolbar h3,
.panel-heading h4 {
  margin: 0;
}

.toolbar p,
.panel-heading p {
  margin: 6px 0 0;
  color: var(--text-secondary);
  font-size: 0.88rem;
}

.import-panel,
.table-panel {
  padding: 20px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-surface);
  box-shadow: var(--shadow-sm);
}

.import-panel {
  margin-bottom: 20px;
}

.panel-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.panel-heading code {
  display: inline-block;
  margin-top: 8px;
  padding: 5px 8px;
  border-radius: 6px;
  background: var(--code-bg);
  color: var(--text-primary);
  font-size: 0.82rem;
  word-break: break-all;
}

.payload-input {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.import-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 14px;
}

.result-panel {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px solid var(--border-soft);
}

.result-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.result-stats span {
  padding: 5px 10px;
  border: 1px solid var(--border-color);
  border-radius: 999px;
  color: var(--text-secondary);
  font-size: 0.82rem;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .import-panel,
  .table-panel {
    padding: 16px;
  }

  .toolbar,
  .panel-heading,
  .import-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
