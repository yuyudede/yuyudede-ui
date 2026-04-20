<template>
  <div class="portal">
    <section class="hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <h1 class="title">yuyudede</h1>
        <p class="subtitle">左转三次等于右转</p>
      </div>
      <div class="scroll-hint">
        <span>探索下方模块</span>
        <div class="arrow">↓</div>
      </div>
    </section>

    <section class="modules-section">
      <div class="modules-grid">
        <component
          :is="m.active && m.link ? 'router-link' : 'div'"
          v-for="(m, i) in modules"
          :key="m.title"
          :to="m.active ? m.link : undefined"
          class="module-card"
          :class="{ active: m.active, inactive: !m.active }"
          :style="{ animationDelay: `${i * 0.1}s` }"
        >
          <div class="card-icon">{{ m.icon }}</div>
          <h3 class="card-title">{{ m.title }}</h3>
          <p class="card-desc">{{ m.desc }}</p>
          <div class="card-badge">
            {{ m.active ? '立即进入 →' : '敬请期待' }}
          </div>
        </component>
      </div>
    </section>
  </div>
</template>

<script setup>
const modules = [
  { icon: '📝', title: '博客', desc: '记录技术与生活', link: '/blog', active: true },
  { icon: '🧰', title: '工具箱', desc: '实用小工具合集', link: null, active: false },
  { icon: '📚', title: '知识库', desc: '笔记与速查', link: null, active: false },
  { icon: '🎨', title: '项目展示', desc: '作品与实验', link: null, active: false },
]
</script>

<style scoped>
.portal {
  min-height: calc(100vh - 120px);
}

/* ===== Hero ===== */
.hero {
  position: relative;
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
  color: #fff;
  padding: 80px 20px 120px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: var(--portal-gradient);
  background-size: 300% 300%;
  animation: gradientShift 18s ease infinite;
  z-index: 0;
}

.hero-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 40%);
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.hero-content {
  position: relative;
  z-index: 1;
  animation: fadeUp 1s ease-out;
}

.title {
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #fff 30%, rgba(255, 255, 255, 0.75));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 16px;
  text-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
}

.subtitle {
  font-size: clamp(1rem, 2vw, 1.4rem);
  opacity: 0.9;
  letter-spacing: 3px;
  font-weight: 300;
}

.scroll-hint {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  opacity: 0.7;
  z-index: 1;
  animation: fadeUp 1s ease-out 0.6s backwards;
}

.scroll-hint .arrow {
  animation: bounce 2s ease-in-out infinite;
  font-size: 1.2rem;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Modules ===== */
.modules-section {
  max-width: 1100px;
  margin: -60px auto 0;
  padding: 0 20px 80px;
  position: relative;
  z-index: 2;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.module-card {
  position: relative;
  padding: 36px 28px;
  border-radius: 20px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
  text-decoration: none;
  color: var(--text-primary);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  opacity: 0;
  cursor: pointer;
  overflow: hidden;
  animation: cardIn 0.6s ease-out forwards;
}

.module-card.inactive {
  cursor: not-allowed;
  filter: grayscale(0.4);
  animation-name: cardInDim;
}

.module-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), transparent);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.module-card.active:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
}

.module-card.active:hover::before {
  opacity: 1;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes cardInDim {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 0.6; transform: translateY(0); }
}

.card-icon {
  font-size: 2.6rem;
  margin-bottom: 16px;
  line-height: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.card-desc {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.card-badge {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 1px;
}

.module-card.inactive .card-badge {
  color: var(--text-secondary);
}

/* ===== Responsive ===== */
@media (max-width: 720px) {
  .modules-grid {
    grid-template-columns: 1fr;
  }
  .hero {
    min-height: 50vh;
    padding: 60px 20px 100px;
  }
  .modules-section {
    margin-top: -40px;
  }
}
</style>
