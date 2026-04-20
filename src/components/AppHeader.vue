<template>
  <el-header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">yuyudede</router-link>
      <el-menu mode="horizontal" :ellipsis="false" class="nav-menu" router>
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/blog">博客</el-menu-item>
      </el-menu>
      <div class="header-right">
        <el-switch v-model="isDark" inline-prompt active-text="🌙" inactive-text="☀️" @change="toggleDark" />
        <router-link v-if="!auth.isAuthenticated" to="/login">
          <el-button type="primary" text>登录</el-button>
        </router-link>
        <el-dropdown v-else>
          <el-button type="primary" text>{{ auth.username }}</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/admin')">管理后台</el-dropdown-item>
              <el-dropdown-item @click="handleLogout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const isDark = ref(false)

function applyDark(val) {
  document.documentElement.classList.toggle('dark', val)
  localStorage.setItem('theme', val ? 'dark' : 'light')
}

function toggleDark(val) {
  applyDark(val)
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = saved ? saved === 'dark' : prefersDark
  applyDark(isDark.value)
})

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.header {
  background: var(--bg-surface);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.3s ease;
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 60px;
}
.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
  margin-right: 40px;
}
.nav-menu {
  border: none;
  flex: 1;
  background: transparent;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
