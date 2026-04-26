<template>
  <div class="toolbox-page">
    <div class="toolbox-hero">
      <h1 class="toolbox-title">工具箱</h1>
      <p class="toolbox-desc">日常开发与效率小工具合集。</p>
    </div>

    <div class="tool-grid">
      <router-link to="/tools/sudoku" class="tool-card theme-sudoku">
        <div class="tool-card-art">
          <div class="art-blur art-a"></div>
          <div class="art-blur art-b"></div>
          <div class="art-blur art-c"></div>
          <div class="art-grain"></div>
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

      <!-- Future tools go here -->
    </div>

    <div v-if="false" class="tool-empty">
      <p>更多工具即将上线...</p>
    </div>
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'

useHead({
  title: '工具箱',
})
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
  animation: fadeUp 0.6s cubic-bezier(0.2,0.8,0.2,1);
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
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  animation: fadeUp 0.6s 0.1s cubic-bezier(0.2,0.8,0.2,1) both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Tool card — reuses portal card style */
.tool-card {
  position: relative;
  display: block;
  padding: 22px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.10);
  box-shadow:
    0 1px 2px rgba(15, 23, 42, 0.03),
    0 8px 24px -10px rgba(15, 23, 42, 0.08);
  text-decoration: none;
  color: var(--text-primary);
  overflow: hidden;
  isolation: isolate;
  cursor: pointer;
  transition: transform 0.45s cubic-bezier(0.2,0.8,0.2,1),
              box-shadow 0.45s cubic-bezier(0.2,0.8,0.2,1),
              border-color 0.45s;
  min-height: 180px;
}
html.dark .tool-card {
  background: rgba(30, 35, 48, 0.28);
  border-color: rgba(120, 140, 180, 0.08);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.12),
    0 8px 24px -12px rgba(0, 0, 0, 0.22);
}

.tool-card::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  background:
    radial-gradient(120% 80% at 100% 0%, rgba(160, 170, 210, 0.05), transparent 62%),
    radial-gradient(120% 80% at 0% 100%, rgba(180, 175, 200, 0.04), transparent 62%);
  pointer-events: none;
}
html.dark .tool-card::after { opacity: 0.4; }

/* Hover art */
.tool-card-art {
  position: absolute;
  inset: 0;
  z-index: 0;
  opacity: 0;
  transform: scale(1.05);
  transition: opacity 0.55s cubic-bezier(0.2,0.8,0.2,1),
              transform 0.8s cubic-bezier(0.2,0.8,0.2,1);
  overflow: hidden;
  border-radius: inherit;
}
.art-blur {
  position: absolute;
  border-radius: 50%;
  filter: blur(24px);
  opacity: 0.85;
}
.art-a { width: 90%; height: 90%; top: -20%; left: -20%; }
.art-b { width: 80%; height: 80%; top: 15%; right: -25%; }
.art-c { width: 70%; height: 70%; bottom: -25%; left: 15%; }
.art-grain {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='1.1' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 40px -10px rgba(15,23,42,0.14);
  border-color: rgba(255, 255, 255, 0.18);
  color: #fff;
}
html.dark .tool-card:hover {
  background: rgba(40, 46, 62, 0.38);
  border-color: rgba(120, 140, 180, 0.14);
}
.tool-card:hover .tool-card-art {
  opacity: 1;
  transform: scale(1);
}
.tool-card:hover .tool-desc {
  color: rgba(255,255,255,0.85);
}

.tool-card-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.tool-icon {
  width: 36px;
  height: 36px;
  color: currentColor;
}
.tool-icon :deep(svg) { width: 100%; height: 100%; }
.tool-name {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.tool-desc {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.55;
  transition: color 0.4s;
}

/* Sudoku theme colors */
.theme-sudoku .art-a { background: #818cf8; }
.theme-sudoku .art-b { background: #a78bfa; }
.theme-sudoku .art-c { background: #22d3ee; }

.tool-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 0;
  color: var(--text-secondary);
}

@media (max-width: 640px) {
  .toolbox-page {
    padding: 24px 16px 60px;
  }
  .tool-grid {
    grid-template-columns: 1fr;
  }
}
</style>
