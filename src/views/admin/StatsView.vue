<template>
  <div class="stats-page">
    <div class="toolbar">
      <h3>接口统计</h3>
      <el-button :icon="Refresh" circle @click="fetchStats" :loading="loading" />
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-value">{{ stats.today }}</div>
        <div class="stat-label">今日请求</div>
      </el-card>
      <el-card class="stat-card" shadow="hover">
        <div class="stat-value">{{ stats.week }}</div>
        <div class="stat-label">本周请求</div>
      </el-card>
      <el-card class="stat-card" shadow="hover">
        <div class="stat-value">{{ stats.month }}</div>
        <div class="stat-label">本月请求</div>
      </el-card>
    </div>

    <!-- 每日趋势 -->
    <el-card class="chart-card" shadow="never" v-loading="loading">
      <template #header>
        <span>每日请求趋势（近 30 天）</span>
      </template>
      <div class="bar-chart">
        <div
          v-for="item in stats.daily"
          :key="item.date"
          class="bar-item"
          :title="`${item.date}: ${item.count}`"
        >
          <div class="bar-fill" :style="{ height: barHeight(item.count) + '%' }"></div>
          <div class="bar-label">{{ formatShortDate(item.date) }}</div>
        </div>
      </div>
    </el-card>

    <!-- 热门路径 -->
    <el-card class="table-card" shadow="never" v-loading="loading">
      <template #header>
        <span>热门接口路径（近 7 天）</span>
      </template>
      <el-table :data="stats.topPaths" stripe>
        <el-table-column type="index" width="60" />
        <el-table-column prop="path" label="路径" min-width="200" show-overflow-tooltip />
        <el-table-column prop="count" label="请求次数" width="120" align="right">
          <template #default="{ row }">
            <el-tag size="small">{{ row.count }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import api from '../../api'

const loading = ref(false)
const stats = ref({
  today: 0,
  week: 0,
  month: 0,
  topPaths: [],
  daily: [],
})

const maxDaily = ref(1)

function barHeight(count) {
  const c = Number(count) || 0
  if (!maxDaily.value || maxDaily.value <= 0) return 0
  return Math.max(4, (c / maxDaily.value) * 100)
}

function formatShortDate(dateStr) {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

async function fetchStats() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/stats/api-usage')
    stats.value = data
    maxDaily.value = Math.max(
      1,
      ...data.daily.map((d) => d.count)
    )
  } catch (err) {
    console.error('Failed to fetch stats:', err)
    ElMessage.error('获取统计数据失败: ' + (err.response?.data?.message || err.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchStats())
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

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card :deep(.el-card__body) {
  text-align: center;
  padding: 24px 16px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
}

.stat-label {
  margin-top: 8px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.chart-card {
  margin-bottom: 20px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 180px;
  padding-bottom: 24px;
  overflow-x: auto;
}

.bar-item {
  flex: 1;
  min-width: 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 4px;
}

.bar-fill {
  width: 100%;
  border-radius: 4px 4px 0 0;
  background: linear-gradient(180deg, #818cf8, #c084fc);
  opacity: 0.85;
  transition: opacity 0.2s;
}

.bar-item:hover .bar-fill {
  opacity: 1;
}

.bar-label {
  font-size: 0.65rem;
  color: var(--text-secondary);
  white-space: nowrap;
  transform: rotate(-45deg);
  transform-origin: top left;
  position: relative;
  top: 8px;
}

.table-card {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }

  .bar-chart {
    height: 140px;
  }
}
</style>
