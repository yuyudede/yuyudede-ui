<template>
  <section class="hero">
    <!-- 磨砂光斑背景 -->
    <div class="ambient">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grain"></div>
    </div>

    <!-- 内容 -->
    <div class="hero-content">
      <div class="badge">
        <span class="badge-dot"></span>
        <span>CODE · CREATE · CURATE</span>
      </div>

      <h1 class="hero-title">
        Welcome to
        <span class="gradient-text">yuyudede's Blog</span>
      </h1>

      <p class="subtitle">记录技术 · 分享生活 · 探索未知</p>

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
  </section>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({ articles: 42, categories: 8, tags: 36, days: 365 })
  }
})

const display = reactive({ articles: 0, categories: 0, tags: 0, days: 0 })

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
  countUp()
})
</script>

<style scoped>
.hero {
  position: relative;
  padding: 80px 20px 60px;
  text-align: center;
  overflow: hidden;
  isolation: isolate;
}

/* 磨砂光斑背景 —— 与 PortalView 一致 */
.ambient {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.55;
  mix-blend-mode: multiply;
  animation: orbFloat 22s ease-in-out infinite;
}
.orb-1 {
  width: 520px; height: 520px;
  top: -140px; left: -120px;
  background: radial-gradient(circle, #c7b8ff, transparent 70%);
}
.orb-2 {
  width: 560px; height: 560px;
  top: 20%; right: -160px;
  background: radial-gradient(circle, #ffb3d6, transparent 70%);
  animation-delay: -7s;
}
.orb-3 {
  width: 440px; height: 440px;
  bottom: -120px; left: 30%;
  background: radial-gradient(circle, #b7e8ff, transparent 70%);
  animation-delay: -14s;
}
:global(html.dark) .orb {
  mix-blend-mode: screen;
  opacity: 0.35;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(40px,-30px) scale(1.08); }
  66% { transform: translate(-30px,40px) scale(0.96); }
}

.grain {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}

/* 内容 */
.hero-content {
  position: relative;
  z-index: 1;
  max-width: 720px;
  margin: 0 auto;
}

/* badge */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 999px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.72rem;
  letter-spacing: 3px;
  color: var(--text-secondary);
  margin-bottom: 28px;
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
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

/* 标题 */
.hero-title {
  font-size: clamp(2.2rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: 16px;
  animation: fadeUp 0.8s 0.2s both;
}
.gradient-text {
  display: block;
  background: linear-gradient(120deg, #8b5cf6, #ec4899 50%, #f59e0b);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* 副标题 */
.subtitle {
  font-size: clamp(0.95rem, 1.4vw, 1.12rem);
  color: var(--text-secondary);
  letter-spacing: 2px;
  margin-bottom: 0;
  animation: fadeUp 0.8s 0.35s both;
}

/* 统计 */
.stats {
  margin-top: 40px;
  display: inline-flex;
  align-items: center;
  gap: 24px;
  padding: 18px 32px;
  border-radius: 18px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
  animation: fadeUp 0.8s 0.5s both;
  flex-wrap: wrap;
  justify-content: center;
}
.stat {
  text-align: center;
  min-width: 72px;
}
.stat-num {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  display: inline-flex;
  align-items: baseline;
}
.plus {
  font-size: 0.9rem;
  color: #8b5cf6;
  margin-left: 2px;
}
.stat-label {
  font-size: 0.65rem;
  letter-spacing: 2px;
  color: var(--text-secondary);
  margin-top: 4px;
}
.stat-divider {
  width: 1px;
  height: 28px;
  background: linear-gradient(180deg, transparent, var(--border-color), transparent);
}

/* CTA */
.cta-group {
  margin-top: 32px;
  display: inline-flex;
  gap: 14px;
  flex-wrap: wrap;
  justify-content: center;
  animation: fadeUp 0.8s 0.65s both;
}
.cta {
  position: relative;
  padding: 12px 24px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.2,0.8,0.2,1);
}
.cta-primary {
  color: #fff;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}
.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(99, 102, 241, 0.4);
}
.cta-primary svg { transition: transform 0.3s; }
.cta-primary:hover svg { transform: translateX(4px); }

.cta-ghost {
  color: var(--text-primary);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.cta-ghost:hover {
  border-color: rgba(139, 92, 246, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.12);
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .hero { padding: 60px 16px 40px; }
  .stats { gap: 16px; padding: 14px 18px; }
  .stat-num { font-size: 1.4rem; }
  .stat-divider { display: none; }
}
</style>
