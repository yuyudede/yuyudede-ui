<template>
  <el-container class="admin-layout">
    <el-aside width="200px" class="admin-aside">
      <div class="admin-logo">管理后台</div>
      <el-menu
        :default-active="activeMenu"
        router
        class="admin-menu"
      >
        <el-menu-item index="/admin/articles">
          <el-icon><Document /></el-icon>
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/comments">
          <el-icon><ChatDotRound /></el-icon>
          <span>评论管理</span>
        </el-menu-item>
      </el-menu>
      <el-divider />
      <router-link to="/" class="back-link">
        <el-icon><Back /></el-icon>
        <span>返回前台</span>
      </router-link>
    </el-aside>
    <el-main class="admin-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Document, ChatDotRound, Back } from '@element-plus/icons-vue'

const route = useRoute()

const activeMenu = computed(() => {
  if (route.path.startsWith('/admin/comments')) return '/admin/comments'
  return '/admin/articles'
})
</script>

<style scoped>
.admin-layout {
  min-height: calc(100vh - 120px);
}

.admin-aside {
  background: #fff;
  border-right: 1px solid #e4e7ed;
  padding-top: 16px;
}

.admin-logo {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 20px;
  padding: 0 20px;
}

.admin-menu {
  border-right: none;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary);
}

.admin-main {
  background: #f5f7fa;
  padding: 24px;
}
</style>
