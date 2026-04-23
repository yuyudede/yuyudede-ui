<template>
  <div class="login-page">
    <div class="login-ambient">
      <div class="login-orb orb-1"></div>
      <div class="login-orb orb-2"></div>
    </div>
    <div class="login-card">
      <div class="login-brand">
        <span class="brand-dot"></span>
        <span class="brand-name">yuyudede</span>
      </div>
      <h2 class="login-title">管理员登录</h2>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <button
            type="submit"
            :disabled="loading"
            class="login-btn"
          >
            <span v-if="loading" class="btn-spinner"></span>
            <span v-else>登录</span>
          </button>
        </el-form-item>
      </el-form>
      <router-link to="/" class="login-back">← 返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const formRef = ref(null)
const loading = ref(false)

const form = ref({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  if (!formRef.value) return
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    const redirect = route.query.redirect || '/admin'
    router.push(redirect)
  } catch {
    ElMessage.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  background: var(--bg-page);
  overflow: hidden;
}

/* 背景光斑 */
.login-ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}
.login-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.45;
}
.orb-1 {
  width: 400px; height: 400px;
  top: -120px; left: -80px;
  background: radial-gradient(circle, #c7b8ff, transparent 70%);
}
.orb-2 {
  width: 360px; height: 360px;
  bottom: -100px; right: -60px;
  background: radial-gradient(circle, #ffb3d6, transparent 70%);
}

/* 登录卡片 - 玻璃拟态 */
.login-card {
  position: relative;
  z-index: 1;
  width: 420px;
  padding: 40px 36px 32px;
  border-radius: 24px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow), 0 20px 60px -20px rgba(15, 23, 42, 0.15);
  animation: fadeUp 0.6s cubic-bezier(0.2,0.8,0.2,1) both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.login-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 28px;
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

.login-title {
  text-align: center;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 28px;
  color: var(--text-primary);
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s, opacity 0.25s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(129, 140, 248, 0.5);
}
.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-back {
  display: block;
  text-align: center;
  margin-top: 20px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
}
.login-back:hover {
  color: #8b5cf6;
}

/* 覆盖 Element Plus 输入框样式以融入玻璃拟态 */
:deep(.el-input__wrapper) {
  background: var(--glass-bg) !important;
  border-radius: 12px !important;
  box-shadow: inset 0 0 0 1px var(--glass-border) !important;
  padding: 4px 12px !important;
}
:deep(.el-input__wrapper.is-focus) {
  box-shadow: inset 0 0 0 1px rgba(139, 92, 246, 0.4) !important;
}
:deep(.el-input__inner) {
  color: var(--text-primary) !important;
}
:deep(.el-input__inner::placeholder) {
  color: var(--text-secondary) !important;
}

@media (max-width: 480px) {
  .login-card {
    width: 90vw;
    padding: 32px 24px 24px;
  }
}
</style>
