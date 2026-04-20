<template>
  <el-header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">yuyudede</router-link>
      <el-menu mode="horizontal" :ellipsis="false" class="nav-menu" router>
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/categories">分类</el-menu-item>
        <el-menu-item index="/tags">标签</el-menu-item>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const isDark = ref(false)

function toggleDark(val) {
  document.documentElement.classList.toggle('dark', val)
}

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
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
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
