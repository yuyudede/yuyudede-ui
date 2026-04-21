<template>
  <section ref="heroEl" class="hero" @mousemove="onMouseMove">
    <!-- 动态极光背景 -->
    <div class="aurora">
      <div class="aurora-blob blob-1"></div>
      <div class="aurora-blob blob-2"></div>
      <div class="aurora-blob blob-3"></div>
    </div>

    <!-- 粒子星网 -->
    <canvas ref="canvasEl" class="particles"></canvas>

    <!-- 噪点纹理 -->
    <div class="noise"></div>

    <!-- 鼠标聚光灯 -->
    <div
      class="spotlight"
      :style="{
        background: `radial-gradient(600px circle at ${mouse.x}px ${mouse.y}px, rgba(255,255,255,0.12), transparent 40%)`
      }"
    ></div>

    <!-- 网格线 -->
    <div class="grid-lines"></div>

    <!-- 内容 -->
    <div class="hero-content">
      <div class="badge">
        <span class="badge-dot"></span>
        <span>CODE · CREATE · CURATE</span>
      </div>

      <h1 class="hero-title">
        <span class="line">
          <span class="word shine" data-text="Welcome">Welcome</span>
          <span class="word" data-text="to">to</span>
        </span>
        <span class="line">
          <span class="word gradient-flow" data-text="yuyudede's">yuyudede's</span>
          <span class="word gradient-flow" data-text="Blog">Blog</span>
        </span>
      </h1>

      <p class="subtitle">
        <span class="glitch" data-text="< 记录技术 · 分享生活 · 探索未知 />">
          &lt; 记录技术 · 分享生活 · 探索未知 /&gt;
        </span>
      </p>

      <!-- 统计 -->
      <div class="stats">
        <div class="stat">
          <div class="stat-num">{{ display.articles }}<span class="plus">+</span></div>
          <div class="stat-label">ARTICLES</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat">
          <div class="stat-num">{{ display.categories }}</div>
          <div class="stat-label">CATEGORIES</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat">
          <div class="stat-num">{{ display.tags }}<span class="plus">+</span></div>
          <div class="stat-label">TAGS</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat">
          <div class="stat-num">{{ display.days }}</div>
          <div class="stat-label">DAYS ONLINE</div>
        </div>
      </div>

      <!-- CTA -->
      <div class="cta-group">
        <a href="#articles" class="cta cta-primary">
          <span>开始阅读</span>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="#about" class="cta cta-ghost">
          <span>了解我</span>
        </a>
      </div>
    </div>

    <!-- 滚动指示 -->
    <div class="scroll-hint">
      <div class="mouse"><div class="wheel"></div></div>
      <span>SCROLL DOWN</span>
    </div>

    <!-- 底部向下渐隐到页面色,避免硬切 -->
    <div class="fade-to-page"></div>

    <!-- 波浪分隔 -->
    <div class="wave">
      <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
        <path d="M0,64 C240,120 480,0 720,48 C960,96 1200,32 1440,72 L1440,120 L0,120 Z" fill="currentColor" opacity="0.9">
          <animate
            attributeName="d"
            dur="10s"
            repeatCount="indefinite"
            values="
              M0,64 C240,120 480,0 720,48 C960,96 1200,32 1440,72 L1440,120 L0,120 Z;
              M0,72 C240,24 480,104 720,80 C960,56 1200,112 1440,56 L1440,120 L0,120 Z;
              M0,64 C240,120 480,0 720,48 C960,96 1200,32 1440,72 L1440,120 L0,120 Z
            "
          />
        </path>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({ articles: 42, categories: 8, tags: 36, days: 365 })
  }
})

const heroEl = ref(null)
const canvasEl = ref(null)
const mouse = reactive({ x: -9999, y: -9999 })
const display = reactive({ articles: 0, categories: 0, tags: 0, days: 0 })

let rafId = null
let particles = []
let ctx = null

function onMouseMove(e) {
  const rect = heroEl.value.getBoundingClientRect()
  mouse.x = e.clientX - rect.left
  mouse.y = e.clientY - rect.top
}

function initCanvas() {
  const canvas = canvasEl.value
  if (!canvas) return
  ctx = canvas.getContext('2d')
  resizeCanvas()

  const count = Math.min(90, Math.floor((canvas.width * canvas.height) / 18000))
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    r: Math.random() * 1.6 + 0.4
  }))

  tick()
}

function resizeCanvas() {
  const canvas = canvasEl.value
  if (!canvas || !heroEl.value) return
  const dpr = window.devicePixelRatio || 1
  const rect = heroEl.value.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  canvas.style.width = rect.width + 'px'
  canvas.style.height = rect.height + 'px'
  ctx && ctx.scale(dpr, dpr)
}

function tick() {
  const canvas = canvasEl.value
  if (!canvas || !ctx) return
  const dpr = window.devicePixelRatio || 1
  const w = canvas.width / dpr
  const h = canvas.height / dpr

  ctx.clearRect(0, 0, w, h)

  // 粒子
  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy
    if (p.x < 0 || p.x > w) p.vx *= -1
    if (p.y < 0 || p.y > h) p.vy *= -1

    // 鼠标引力
    const dx = mouse.x - p.x
    const dy = mouse.y - p.y
    const dist = Math.hypot(dx, dy)
    if (dist < 160) {
      p.x += (dx / dist) * 0.4
      p.y += (dy / dist) * 0.4
    }

    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fillStyle = 'rgba(255,255,255,0.75)'
    ctx.fill()
  }

  // 连线
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const a = particles[i]
      const b = particles[j]
      const dx = a.x - b.x
      const dy = a.y - b.y
      const d = Math.hypot(dx, dy)
      if (d < 120) {
        ctx.beginPath()
        ctx.moveTo(a.x, a.y)
        ctx.lineTo(b.x, b.y)
        ctx.strokeStyle = `rgba(255,255,255,${(1 - d / 120) * 0.25})`
        ctx.lineWidth = 0.6
        ctx.stroke()
      }
    }
    // 鼠标连线
    const dx = particles[i].x - mouse.x
    const dy = particles[i].y - mouse.y
    const d = Math.hypot(dx, dy)
    if (d < 160) {
      ctx.beginPath()
      ctx.moveTo(particles[i].x, particles[i].y)
      ctx.lineTo(mouse.x, mouse.y)
      ctx.strokeStyle = `rgba(147,197,253,${(1 - d / 160) * 0.6})`
      ctx.lineWidth = 0.8
      ctx.stroke()
    }
  }

  rafId = requestAnimationFrame(tick)
}

// 数字滚动
function countUp() {
  const duration = 1800
  const start = performance.now()
  const from = { articles: 0, categories: 0, tags: 0, days: 0 }
  const to = props.stats
  const ease = (t) => 1 - Math.pow(1 - t, 3)
  function step(now) {
    const p = Math.min(1, (now - start) / duration)
    const k = ease(p)
    display.articles = Math.round(from.articles + (to.articles - from.articles) * k)
    display.categories = Math.round(from.categories + (to.categories - from.categories) * k)
    display.tags = Math.round(from.tags + (to.tags - from.tags) * k)
    display.days = Math.round(from.days + (to.days - from.days) * k)
    if (p < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => {
  initCanvas()
  countUp()
  window.addEventListener('resize', resizeCanvas)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  window.removeEventListener('resize', resizeCanvas)
})
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 90vh;
  padding: 120px 20px 140px;
  text-align: center;
  color: #fff;
  overflow: hidden;
  isolation: isolate;
  background:
    radial-gradient(ellipse at top, #1e1b4b 0%, #0f0c29 40%, #05030f 100%);
}

/* 极光背景 */
.aurora {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  filter: blur(60px);
  opacity: 0.9;
}
.aurora-blob {
  position: absolute;
  border-radius: 50%;
  mix-blend-mode: screen;
  animation: blobFloat 20s ease-in-out infinite;
}
.blob-1 {
  width: 560px; height: 560px;
  top: -160px; left: -120px;
  background: radial-gradient(circle, #6366f1, transparent 70%);
}
.blob-2 {
  width: 640px; height: 640px;
  top: 20%; right: -160px;
  background: radial-gradient(circle, #ec4899, transparent 70%);
  animation-delay: -6s;
}
.blob-3 {
  width: 520px; height: 520px;
  bottom: -160px; left: 30%;
  background: radial-gradient(circle, #22d3ee, transparent 70%);
  animation-delay: -12s;
}
@keyframes blobFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(60px,-40px) scale(1.1); }
  66% { transform: translate(-40px,60px) scale(0.95); }
}

/* 粒子 */
.particles {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

/* 聚光灯 */
.spotlight {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  transition: background 0.1s;
}

/* 网格 */
.grid-lines {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
}

/* 噪点 */
.noise {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  opacity: 0.06;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.8'/></svg>");
}

.hero-content {
  position: relative;
  z-index: 3;
  max-width: 920px;
  margin: 0 auto;
}

/* badge */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  font-size: 0.75rem;
  letter-spacing: 3px;
  color: rgba(255,255,255,0.85);
  margin-bottom: 32px;
  animation: fadeUp 0.8s 0.1s both;
}
.badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #22d3ee;
  box-shadow: 0 0 10px #22d3ee, 0 0 20px #22d3ee;
  animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

/* 标题 */
.hero-title {
  font-size: clamp(2.4rem, 6vw, 5rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}
.line { display: block; }
.word {
  display: inline-block;
  margin: 0 0.15em;
  animation: wordIn 0.8s cubic-bezier(0.2,0.8,0.2,1) both;
}
.word:nth-child(1) { animation-delay: 0.15s; }
.word:nth-child(2) { animation-delay: 0.3s; }
.line:nth-child(2) .word:nth-child(1) { animation-delay: 0.45s; }
.line:nth-child(2) .word:nth-child(2) { animation-delay: 0.6s; }

@keyframes wordIn {
  from { opacity: 0; transform: translateY(30px) rotateX(-40deg); filter: blur(8px); }
  to { opacity: 1; transform: translateY(0) rotateX(0); filter: blur(0); }
}

.gradient-flow {
  background: linear-gradient(110deg, #818cf8 0%, #f472b6 25%, #fbbf24 50%, #34d399 75%, #22d3ee 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: wordIn 0.8s cubic-bezier(0.2,0.8,0.2,1) both, gradientShift 6s ease infinite;
  filter: drop-shadow(0 0 30px rgba(129,140,248,0.35));
}
@keyframes gradientShift {
  0%,100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.shine {
  position: relative;
  color: #fff;
}
.shine::after {
  content: attr(data-text);
  position: absolute; inset: 0;
  background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.9) 50%, transparent 70%);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: shine 3.5s linear infinite;
}
@keyframes shine {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}

/* 副标题 glitch */
.subtitle {
  margin-top: 8px;
  font-size: clamp(1rem, 1.6vw, 1.2rem);
  color: rgba(255,255,255,0.75);
  letter-spacing: 2px;
  font-family: 'JetBrains Mono', 'SF Mono', Menlo, monospace;
  animation: fadeUp 0.8s 0.9s both;
}
.glitch {
  position: relative;
  display: inline-block;
}
.glitch::before, .glitch::after {
  content: attr(data-text);
  position: absolute; left: 0; top: 0;
  width: 100%; overflow: hidden;
}
.glitch::before {
  color: #22d3ee;
  clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
  animation: glitchTop 3s infinite linear alternate-reverse;
}
.glitch::after {
  color: #ec4899;
  clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%);
  animation: glitchBot 2.3s infinite linear alternate-reverse;
}
@keyframes glitchTop {
  0%,90%,100% { transform: translate(0); }
  92% { transform: translate(-2px, -1px); }
  94% { transform: translate(2px, 1px); }
}
@keyframes glitchBot {
  0%,88%,100% { transform: translate(0); }
  90% { transform: translate(2px, 1px); }
  93% { transform: translate(-2px, -1px); }
}

/* 统计 */
.stats {
  margin-top: 48px;
  display: inline-flex;
  align-items: center;
  gap: 28px;
  padding: 20px 36px;
  border-radius: 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
  animation: fadeUp 0.8s 1.1s both;
  flex-wrap: wrap;
  justify-content: center;
}
.stat {
  text-align: center;
  min-width: 80px;
}
.stat-num {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(180deg, #fff, #cbd5e1);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-variant-numeric: tabular-nums;
  display: inline-flex;
  align-items: baseline;
}
.plus {
  font-size: 1rem;
  color: #818cf8;
  margin-left: 2px;
}
.stat-label {
  font-size: 0.7rem;
  letter-spacing: 2px;
  color: rgba(255,255,255,0.5);
  margin-top: 4px;
}
.stat-divider {
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, transparent, rgba(255,255,255,0.25), transparent);
}

/* CTA */
.cta-group {
  margin-top: 40px;
  display: inline-flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
  animation: fadeUp 0.8s 1.3s both;
}
.cta {
  position: relative;
  padding: 14px 28px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.2,0.8,0.2,1);
  overflow: hidden;
}
.cta-primary {
  color: #0f0c29;
  background: linear-gradient(110deg, #fff, #e0e7ff, #fff);
  background-size: 200% 100%;
  box-shadow: 0 8px 30px rgba(255,255,255,0.25), 0 0 0 1px rgba(255,255,255,0.4);
}
.cta-primary:hover {
  background-position: 100% 0;
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(129,140,248,0.5), 0 0 0 1px rgba(255,255,255,0.6);
}
.cta-primary svg { transition: transform 0.3s; }
.cta-primary:hover svg { transform: translateX(4px); }

.cta-ghost {
  color: #fff;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
}
.cta-ghost:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.4);
  transform: translateY(-2px);
}

/* 滚动提示 */
.scroll-hint {
  position: absolute;
  bottom: 120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: rgba(255,255,255,0.6);
  font-size: 0.7rem;
  letter-spacing: 3px;
  animation: fadeUp 0.8s 1.6s both;
}
.mouse {
  width: 22px;
  height: 36px;
  border: 2px solid rgba(255,255,255,0.6);
  border-radius: 12px;
  display: flex;
  justify-content: center;
  padding-top: 6px;
}
.wheel {
  width: 3px;
  height: 8px;
  background: #fff;
  border-radius: 2px;
  animation: wheel 1.6s ease-in-out infinite;
}
@keyframes wheel {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(10px); opacity: 0; }
}

/* 底部柔化过渡 */
.fade-to-page {
  position: absolute;
  left: 0; right: 0;
  bottom: 0;
  height: 280px;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(15, 12, 41, 0.25) 35%,
    rgba(30, 27, 75, 0.55) 65%,
    var(--bg-page) 100%
  );
}

/* 波浪 */
.wave {
  position: absolute;
  bottom: -1px; left: 0;
  width: 100%;
  line-height: 0;
  z-index: 3;
  color: var(--bg-page);
}
.wave svg {
  width: 100%;
  height: 120px;
  display: block;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .stats { gap: 16px; padding: 16px 20px; }
  .stat-num { font-size: 1.5rem; }
  .stat-divider { display: none; }
  .scroll-hint { bottom: 140px; }
}
</style>
