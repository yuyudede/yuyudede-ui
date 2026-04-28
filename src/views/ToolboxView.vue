<template>
  <div class="toolbox-page">
    <section class="toolbox-hero">
      <p class="eyebrow">Toolbox</p>
      <h1 class="toolbox-title">工具箱</h1>
      <p class="toolbox-desc">日常开发与效率小工具合集。</p>
    </section>

    <section class="tool-grid">
      <router-link to="/tools/sudoku" class="tool-card theme-sudoku">
        <div class="tool-card-art">
          <div class="art-blur art-a"></div>
          <div class="art-blur art-b"></div>
          <div class="art-blur art-c"></div>
        </div>
        <div class="tool-card-inner">
          <div class="tool-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <h3 class="tool-name">数独</h3>
          <p class="tool-desc">经典九宫格数字推理游戏，多种难度可选。</p>
        </div>
      </router-link>

      <article class="tool-panel">
        <div class="panel-head">
          <h2>时间戳转换</h2>
          <button @click="useNow">现在</button>
        </div>
        <label>
          Unix 时间戳
          <input v-model="timestampInput" inputmode="numeric" placeholder="1714276800 或 1714276800000" />
        </label>
        <div class="result-box">
          <span>{{ timestampResult }}</span>
        </div>
      </article>

      <article class="tool-panel wide">
        <div class="panel-head">
          <h2>JSON 格式化</h2>
          <button @click="formatJson">格式化</button>
        </div>
        <textarea v-model="jsonInput" spellcheck="false" placeholder='{"hello":"yuyudede"}'></textarea>
        <div class="result-box code" :class="{ error: jsonError }">
          <pre>{{ jsonError || jsonOutput }}</pre>
        </div>
      </article>

      <article class="tool-panel">
        <div class="panel-head">
          <h2>颜色预览</h2>
          <button @click="copyColor">{{ copied ? '已复制' : '复制' }}</button>
        </div>
        <label>
          HEX
          <input v-model="colorInput" placeholder="#818cf8" />
        </label>
        <div class="color-preview" :style="{ background: normalizedColor }"></div>
        <div class="result-box">
          <span>{{ normalizedColor }}</span>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useHead } from '@unhead/vue'

useHead({
  title: '工具箱 - yuyudede',
})

const timestampInput = ref(String(Math.floor(Date.now() / 1000)))
const jsonInput = ref('{\n  "hello": "yuyudede"\n}')
const jsonOutput = ref('')
const jsonError = ref('')
const colorInput = ref('#818cf8')
const copied = ref(false)

const timestampResult = computed(() => {
  const raw = timestampInput.value.trim()
  if (!raw) return '等待输入'
  const num = Number(raw)
  if (!Number.isFinite(num)) return '时间戳格式不正确'
  const ms = raw.length <= 10 ? num * 1000 : num
  const date = new Date(ms)
  if (Number.isNaN(date.getTime())) return '时间戳格式不正确'
  return date.toLocaleString('zh-CN', { hour12: false })
})

const normalizedColor = computed(() => {
  const raw = colorInput.value.trim()
  const value = raw.startsWith('#') ? raw : `#${raw}`
  return /^#[0-9a-fA-F]{6}$/.test(value) ? value : '#818cf8'
})

function useNow() {
  timestampInput.value = String(Math.floor(Date.now() / 1000))
}

function formatJson() {
  try {
    jsonOutput.value = JSON.stringify(JSON.parse(jsonInput.value), null, 2)
    jsonError.value = ''
  } catch (err) {
    jsonError.value = err.message
  }
}

async function copyColor() {
  await navigator.clipboard.writeText(normalizedColor.value)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 1200)
}

watch(jsonInput, () => {
  if (jsonError.value) formatJson()
})

formatJson()
</script>

<style scoped>
.toolbox-page {
  max-width: 1180px;
  margin: 0 auto;
  padding: 48px 28px 80px;
  min-height: calc(100vh - 64px);
}

.toolbox-hero {
  text-align: center;
  padding: 32px 0 40px;
}

.eyebrow {
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.toolbox-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}

.toolbox-desc {
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.tool-card,
.tool-panel {
  position: relative;
  border-radius: 18px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
}

.tool-card {
  display: block;
  min-height: 220px;
  padding: 22px;
  text-decoration: none;
  color: var(--text-primary);
  isolation: isolate;
  transition: transform 0.3s, box-shadow 0.3s;
}

.tool-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 44px -14px rgba(15,23,42,0.2);
  color: #fff;
}

.tool-card-art {
  position: absolute;
  inset: 0;
  z-index: 0;
  opacity: 0;
  transition: opacity 0.4s;
}

.tool-card:hover .tool-card-art {
  opacity: 1;
}

.art-blur {
  position: absolute;
  border-radius: 50%;
  filter: blur(26px);
  opacity: 0.85;
}

.art-a { width: 90%; height: 90%; top: -20%; left: -20%; }
.art-b { width: 80%; height: 80%; top: 15%; right: -25%; }
.art-c { width: 70%; height: 70%; bottom: -25%; left: 15%; }
.theme-sudoku .art-a { background: #818cf8; }
.theme-sudoku .art-b { background: #a78bfa; }
.theme-sudoku .art-c { background: #22d3ee; }

.tool-card-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-icon {
  width: 38px;
  height: 38px;
}

.tool-name {
  font-size: 1.25rem;
  font-weight: 700;
}

.tool-desc {
  color: var(--text-secondary);
  line-height: 1.55;
}

.tool-card:hover .tool-desc {
  color: rgba(255,255,255,0.85);
}

.tool-panel {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.tool-panel.wide {
  grid-column: span 2;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-head h2 {
  font-size: 1rem;
  margin: 0;
}

.panel-head button,
.tool-panel button {
  border: 1px solid var(--glass-border);
  background: var(--bg-surface);
  color: var(--text-primary);
  border-radius: 10px;
  padding: 7px 12px;
  cursor: pointer;
}

label {
  display: grid;
  gap: 7px;
  color: var(--text-secondary);
  font-size: 0.82rem;
}

input,
textarea {
  width: 100%;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-surface);
  color: var(--text-primary);
  font: inherit;
  padding: 11px 12px;
  outline: none;
}

textarea {
  min-height: 120px;
  resize: vertical;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
  font-size: 0.86rem;
}

.result-box {
  min-height: 44px;
  display: flex;
  align-items: center;
  border-radius: 12px;
  background: var(--bg-surface-2);
  border: 1px solid var(--border-soft);
  color: var(--text-primary);
  padding: 12px;
  overflow: auto;
}

.result-box.code {
  align-items: flex-start;
  max-height: 220px;
}

.result-box.error {
  color: #ef4444;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
  font-size: 0.84rem;
}

.color-preview {
  height: 72px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
}

@media (max-width: 900px) {
  .tool-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .toolbox-page {
    padding: 24px 16px 60px;
  }
  .tool-grid {
    grid-template-columns: 1fr;
  }
  .tool-panel.wide {
    grid-column: span 1;
  }
}
</style>
