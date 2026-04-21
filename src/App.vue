<template>
  <div id="app">
    <!-- 顶部渐变滚动进度条 -->
    <div class="scroll-progress" :style="{ transform: `scaleX(${progress})` }"></div>

    <!-- 自定义鼠标光标 -->
    <div
      class="cursor-dot"
      :class="{ active: cursor.active }"
      :style="{ transform: `translate3d(${cursor.x}px, ${cursor.y}px, 0)` }"
    ></div>
    <div
      class="cursor-ring"
      :class="{ active: cursor.active }"
      :style="{ transform: `translate3d(${cursor.rx}px, ${cursor.ry}px, 0)` }"
    ></div>

    <AppHeader />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, onBeforeUnmount } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'

const progress = ref(0)
const cursor = reactive({ x: -100, y: -100, rx: -100, ry: -100, active: false })

let rafId = null
const target = { x: -100, y: -100 }
const isTouch = (typeof window !== 'undefined') && ('ontouchstart' in window)

function onScroll() {
  const h = document.documentElement
  const max = h.scrollHeight - h.clientHeight
  progress.value = max > 0 ? Math.min(1, h.scrollTop / max) : 0
}

function onMove(e) {
  target.x = e.clientX
  target.y = e.clientY
  cursor.x = e.clientX
  cursor.y = e.clientY
}

function onOver(e) {
  const t = e.target
  if (t && t.closest && t.closest('a, button, .article-card, .cta, [role="button"], .tag-link, .category-item, .social, input, textarea')) {
    cursor.active = true
  } else {
    cursor.active = false
  }
}

function tick() {
  // 环形光标用缓动跟随
  cursor.rx += (target.x - cursor.rx) * 0.18
  cursor.ry += (target.y - cursor.ry) * 0.18
  rafId = requestAnimationFrame(tick)
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
  if (!isTouch) {
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseover', onOver)
    document.body.classList.add('has-custom-cursor')
    rafId = requestAnimationFrame(tick)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseover', onOver)
  cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.main-content {
  min-height: calc(100vh - 120px);
}

/* 顶部进度条 */
.scroll-progress {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #818cf8, #ec4899, #fbbf24, #22d3ee);
  background-size: 200% 100%;
  transform-origin: left center;
  transform: scaleX(0);
  transition: transform 0.12s linear;
  z-index: 9999;
  animation: progressShift 3s linear infinite;
  box-shadow: 0 0 12px rgba(129,140,248,0.6);
}
@keyframes progressShift {
  0% { background-position: 0 0; }
  100% { background-position: 200% 0; }
}

/* 自定义光标 */
.cursor-dot,
.cursor-ring {
  position: fixed;
  top: 0; left: 0;
  pointer-events: none;
  z-index: 9998;
  transition: width 0.25s, height 0.25s, background 0.25s, opacity 0.25s;
  mix-blend-mode: difference;
}
.cursor-dot {
  width: 8px; height: 8px;
  margin: -4px 0 0 -4px;
  border-radius: 50%;
  background: #fff;
}
.cursor-ring {
  width: 36px; height: 36px;
  margin: -18px 0 0 -18px;
  border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.8);
}
.cursor-dot.active { width: 4px; height: 4px; margin: -2px 0 0 -2px; }
.cursor-ring.active {
  width: 54px; height: 54px;
  margin: -27px 0 0 -27px;
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,1);
}

@media (hover: none), (max-width: 768px) {
  .cursor-dot, .cursor-ring { display: none; }
}

/* 页面切换 */
.page-enter-active, .page-leave-active {
  transition: opacity 0.35s ease, transform 0.35s cubic-bezier(0.2,0.8,0.2,1);
}
.page-enter-from {
  opacity: 0;
  transform: translateY(16px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}
</style>
