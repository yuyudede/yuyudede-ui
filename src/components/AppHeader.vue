<template>
  <header class="header" :class="{ scrolled }">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span class="logo-dot"></span>
        <span>yuyudede</span>
      </router-link>

      <nav class="nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <div class="header-right">
        <button
          class="theme-toggle"
          @click="toggleDark(!isDark)"
          :aria-label="isDark ? '切换到亮色' : '切换到暗色'"
        >
          <svg v-if="isDark" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="4"/>
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <router-link v-if="!auth.isAuthenticated" to="/login" class="auth-btn">
          登录
        </router-link>
        <div v-else class="user-wrap" @click="userMenuOpen = !userMenuOpen" v-click-outside="() => userMenuOpen = false">
          <button class="auth-btn">
            {{ auth.username }}
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <transition name="menu">
            <div v-if="userMenuOpen" class="user-menu">
              <button class="menu-item" @click.stop="goAdmin">管理后台</button>
              <button class="menu-item" @click.stop="handleLogout">退出</button>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const isDark = ref(false)
const scrolled = ref(false)
const userMenuOpen = ref(false)

const navItems = [
  { path: '/', label: '首页' },
  { path: '/blog', label: '博客' },
  { path: '/tools', label: '工具箱' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function applyDark(val) {
  document.documentElement.classList.toggle('dark', val)
  localStorage.setItem('theme', val ? 'dark' : 'light')
}

function toggleDark(val) {
  isDark.value = val
  applyDark(val)
}

function goAdmin() {
  userMenuOpen.value = false
  router.push('/admin')
}

function handleLogout() {
  userMenuOpen.value = false
  auth.logout()
  router.push('/')
}

function onScroll() {
  scrolled.value = window.scrollY > 8
}

const vClickOutside = {
  mounted(el, binding) {
    el._handler = (e) => { if (!el.contains(e.target)) binding.value() }
    document.addEventListener('click', el._handler)
  },
  unmounted(el) {
    document.removeEventListener('click', el._handler)
  }
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = saved ? saved === 'dark' : prefersDark
  applyDark(isDark.value)
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  border-bottom: 1px solid transparent;
  transition: background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}
.header.scrolled {
  background: rgba(255, 255, 255, 0.72);
  border-bottom-color: var(--glass-border);
  box-shadow: 0 1px 12px rgba(15, 23, 42, 0.04);
}
:global(html.dark) .header {
  background: rgba(13, 17, 23, 0.5);
}
:global(html.dark) .header.scrolled {
  background: rgba(13, 17, 23, 0.65);
  border-bottom-color: rgba(120, 140, 180, 0.15);
  box-shadow: 0 1px 12px rgba(0, 0, 0, 0.2);
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 64px;
  padding: 0 28px;
  gap: 24px;
}

/* Logo */
.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-primary);
  text-decoration: none;
  white-space: nowrap;
}
.logo-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #ec4899 60%, #f59e0b);
  box-shadow: 0 0 12px rgba(139,92,246,0.45);
}

/* Nav */
.nav {
  flex: 1;
  display: flex;
  gap: 4px;
}
.nav-link {
  position: relative;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 0.92rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.25s, background 0.25s;
}
.nav-link:hover {
  color: var(--text-primary);
  background: rgba(139,92,246,0.08);
}
.nav-link.active {
  color: var(--text-primary);
  background: var(--glass-bg);
  box-shadow: inset 0 0 0 1px var(--glass-border);
}

/* Right side */
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.theme-toggle {
  width: 36px; height: 36px;
  border-radius: 999px;
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: var(--text-primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s, border-color 0.25s, color 0.25s;
}
.theme-toggle:hover {
  transform: rotate(15deg);
  color: #8b5cf6;
  border-color: rgba(139,92,246,0.45);
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: var(--text-primary);
  color: var(--bg-page);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s, opacity 0.25s;
}
.auth-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(15,23,42,0.4);
  opacity: 0.92;
}

/* User dropdown */
.user-wrap {
  position: relative;
}
.user-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 140px;
  padding: 6px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 12px 40px -8px rgba(15,23,42,0.25);
  display: flex;
  flex-direction: column;
  gap: 2px;
  z-index: 10;
}
.menu-item {
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  text-align: left;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}
.menu-item:hover { background: rgba(139,92,246,0.1); }

.menu-enter-active, .menu-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.menu-enter-from, .menu-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

@media (max-width: 640px) {
  .header-inner { padding: 0 16px; gap: 12px; }
  .logo span:last-child { display: none; }
  .nav-link { padding: 6px 10px; font-size: 0.85rem; }
}
</style>
