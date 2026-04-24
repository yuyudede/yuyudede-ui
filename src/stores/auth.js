import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

function parseJwtExp(tokenStr) {
  if (!tokenStr) return null
  try {
    const payload = JSON.parse(atob(tokenStr.split('.')[1]))
    return payload.exp ? payload.exp * 1000 : null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const isAuthenticated = computed(() => {
    if (!token.value) return false
    const exp = parseJwtExp(token.value)
    return exp ? Date.now() < exp : false
  })

  async function login(user, pass) {
    const { data } = await api.post('/auth/login', { username: user, password: pass })
    token.value = data.token
    username.value = data.username
    localStorage.setItem('token', data.token)
    localStorage.setItem('username', data.username)
  }

  function logout() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, isAuthenticated, login, logout }
})
