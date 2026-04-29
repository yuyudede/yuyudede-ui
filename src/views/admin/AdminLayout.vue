<template>
  <div class="admin-layout">
    <aside class="admin-aside">
      <div class="admin-brand">
        <span class="brand-dot"></span>
        <span class="brand-name">管理后台</span>
      </div>
      <nav class="admin-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: activeMenu === item.path }"
        >
          <component :is="item.icon" class="nav-icon" />
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="admin-divider"></div>
      <router-link to="/" class="back-link">
        <Back class="nav-icon" />
        <span>返回前台</span>
      </router-link>
    </aside>
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Document, ChatDotRound, Back, Collection, Odometer, Cpu } from '@element-plus/icons-vue'

const route = useRoute()

const menuItems = [
  { path: '/admin/articles', label: '文章管理', icon: Document },
  { path: '/admin/categories', label: '分类管理', icon: Collection },
  { path: '/admin/comments', label: '评论管理', icon: ChatDotRound },
  { path: '/admin/codex', label: 'Codex 导入', icon: Cpu },
  { path: '/admin/stats', label: '接口统计', icon: Odometer },
]

const activeMenu = computed(() => {
  if (route.path.startsWith('/admin/stats')) return '/admin/stats'
  if (route.path.startsWith('/admin/codex')) return '/admin/codex'
  if (route.path.startsWith('/admin/comments')) return '/admin/comments'
  if (route.path.startsWith('/admin/categories')) return '/admin/categories'
  return '/admin/articles'
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: calc(100vh - 64px);
}

/* 侧边栏 - 玻璃拟态风格 */
.admin-aside {
  width: 220px;
  flex-shrink: 0;
  padding: 24px 16px;
  background: var(--glass-bg);
  border-right: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  display: flex;
  flex-direction: column;
}

.admin-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 12px 20px;
}
.brand-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #ec4899 60%, #f59e0b);
  box-shadow: 0 0 12px rgba(139,92,246,0.45);
}
.brand-name {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-primary);
}

/* 自定义导航 */
.admin-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.25s;
}
.nav-item:hover {
  color: var(--text-primary);
  background: rgba(139, 92, 246, 0.08);
}
.nav-item.active {
  color: #fff;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  box-shadow: 0 4px 16px -4px rgba(129, 140, 248, 0.4);
}
.nav-icon {
  width: 18px;
  height: 18px;
}

.admin-divider {
  height: 1px;
  background: var(--border-soft);
  margin: 16px 12px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.25s;
}
.back-link:hover {
  color: var(--text-primary);
  background: rgba(139, 92, 246, 0.08);
}

.admin-main {
  flex: 1;
  padding: 32px;
  background: var(--bg-page);
  overflow: auto;
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }
  .admin-aside {
    width: 100%;
    flex-direction: row;
    align-items: center;
    padding: 12px 16px;
  }
  .admin-brand { padding: 0; margin-right: 16px; }
  .admin-nav { flex-direction: row; flex: 1; }
  .admin-divider { display: none; }
  .back-link { margin-left: auto; }
  .admin-main { padding: 20px; }
}
</style>
