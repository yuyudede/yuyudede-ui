<template>
  <div class="portal">
    <!-- 背景磨砂光斑层 -->
    <div class="ambient">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grain"></div>
    </div>

    <!-- Hero -->
    <section class="hero">
      <h1 class="title" :class="{ rainbow: titleRainbow }" @click="playTitle">
        <span
          v-for="(ch, i) in titleChars"
          :key="i"
          class="char"
          :class="{ jump: titleJump }"
          :style="{ '--d': i * 0.04 + 's' }"
        >{{ ch }}</span><span class="dot" :class="{ pop: titleJump }">.
          <span class="ripple" v-for="r in ripples" :key="r"></span>
        </span>
      </h1>
      <p class="subtitle">左转三次等于右转。</p>
    </section>

    <!-- 公告条 -->
    <a class="announce" href="/blog">
      <div class="announce-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="4 17 10 11 4 5"/>
          <line x1="12" y1="19" x2="20" y2="19"/>
        </svg>
      </div>
      <div class="announce-text">
        <div class="announce-title">New: 博客上线</div>
        <div class="announce-desc">记录日常技术笔记、源码阅读与小项目实验。</div>
      </div>
      <svg class="announce-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="9 18 15 12 9 6"/>
      </svg>
    </a>

    <!-- 模块网格 -->
    <section class="modules">
      <component
        :is="m.active && m.link ? 'router-link' : 'div'"
        v-for="m in modules"
        :key="m.title"
        :to="m.active ? m.link : undefined"
        class="card"
        :class="[m.theme, { inactive: !m.active }]"
      >
        <!-- hover 时显示的磨砂彩图 -->
        <div class="card-art">
          <div class="art-blur art-a"></div>
          <div class="art-blur art-b"></div>
          <div class="art-blur art-c"></div>
          <div class="art-grain"></div>
        </div>

        <div class="card-inner">
          <div class="card-top">
            <div class="card-icon" v-html="m.icon"></div>
          </div>
          <div class="card-bottom">
            <h3 class="card-title">{{ m.title }}</h3>
            <p class="card-desc">{{ m.desc }}</p>
          </div>
        </div>

        <span class="status-dot" v-if="!m.active"></span>
      </component>
    </section>

    <!-- 底部分组链接 -->
    <section class="foot-grid">
      <div class="foot-col">
        <div class="foot-head">EXPLORE</div>
        <router-link to="/blog" class="foot-link">All posts<span>↗</span></router-link>
        <router-link to="/categories" class="foot-link">Categories<span>↗</span></router-link>
        <router-link to="/tags" class="foot-link">Tags<span>↗</span></router-link>
      </div>
      <div class="foot-col">
        <div class="foot-head">CONNECT</div>
        <a class="foot-link" href="#">GitHub<span>↗</span></a>
        <a class="foot-link" href="#">Email<span>↗</span></a>
        <a class="foot-link" href="#">RSS<span>↗</span></a>
      </div>
      <div class="foot-col">
        <div class="foot-head">ABOUT</div>
        <a class="foot-link" href="#">关于我<span>↗</span></a>
        <a class="foot-link" href="#">友链<span>↗</span></a>
        <a class="foot-link" href="#">留言板<span>↗</span></a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const titleChars = 'yuyudede'.split('')
const titleJump = ref(false)
const titleRainbow = ref(false)
const ripples = ref([])
let rippleId = 0

function playTitle() {
  // 字母跳动
  titleJump.value = false
  titleRainbow.value = false
  requestAnimationFrame(() => {
    titleJump.value = true
    titleRainbow.value = true
  })
  // ripple 水波
  const id = ++rippleId
  ripples.value.push(id)
  setTimeout(() => {
    ripples.value = ripples.value.filter(r => r !== id)
  }, 900)
  // 动画结束复位,便于下次重新触发
  setTimeout(() => {
    titleJump.value = false
    titleRainbow.value = false
  }, 900)
}

const modules = [
  {
    title: '博客',
    desc: '记录技术心得、源码笔记与生活琐碎。',
    link: '/blog',
    active: true,
    theme: 'theme-aurora',
    icon: `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'>
      <path d='M4 6h16M4 12h10M4 18h16' stroke-linecap='round'/></svg>`
  },
  {
    title: '工具箱',
    desc: '日常开发与效率小工具合集。',
    link: null,
    active: false,
    theme: 'theme-citrus',
    icon: `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'>
      <path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.7-3.7a6 6 0 0 1-7.9 7.9L6.4 21a2.1 2.1 0 1 1-3-3l7.5-7.5a6 6 0 0 1 7.9-7.9l-3.7 3.7z'/></svg>`
  },
  {
    title: '知识库',
    desc: '结构化的笔记、速查与体系化整理。',
    link: null,
    active: false,
    theme: 'theme-violet',
    icon: `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'>
      <path d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20'/>
      <path d='M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z'/></svg>`
  },
  {
    title: '项目展示',
    desc: '作品、side project 与实验田。',
    link: null,
    active: false,
    theme: 'theme-sunset',
    icon: `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'>
      <circle cx='12' cy='12' r='3'/>
      <path d='M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3 1.6 1.6 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-1-1.5 1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 9a1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 9 4.6h0a1.6 1.6 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8v0a1.6 1.6 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z'/></svg>`
  },
]
</script>

<style scoped>
/* =========================
   Portal base
========================= */
.portal {
  position: relative;
  max-width: 1180px;
  margin: 0 auto;
  padding: 72px 28px 100px;
  min-height: calc(100vh - 120px);
}

/* 背景磨砂光斑 */
.ambient {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
  border-radius: inherit;
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
html.dark .orb { mix-blend-mode: screen; opacity: 0.35; }

@keyframes orbFloat {
  0%,100% { transform: translate(0,0) scale(1); }
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

/* =========================
   Hero
========================= */
.hero {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 60px 0 56px;
}
.title {
  font-size: clamp(3.5rem, 9vw, 6.5rem);
  font-weight: 700;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 18px;
  animation: fadeUp 0.8s cubic-bezier(0.2,0.8,0.2,1) both;
  cursor: pointer;
  user-select: none;
  display: inline-block;
  position: relative;
}
.title .char {
  display: inline-block;
  transition: color 0.5s ease;
  will-change: transform;
}
.title:hover .char {
  animation: hoverWave 1.2s ease-in-out infinite;
  animation-delay: var(--d);
}
@keyframes hoverWave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* 点击:字母依次跳起 + 彩虹渐变 */
.title .char.jump {
  animation: charJump 0.7s cubic-bezier(0.3,1.6,0.5,1) both;
  animation-delay: var(--d);
}
@keyframes charJump {
  0% { transform: translateY(0) scale(1); }
  40% { transform: translateY(-26px) scale(1.15) rotate(-8deg); }
  70% { transform: translateY(4px) scale(0.92); }
  100% { transform: translateY(0) scale(1); }
}

.title.rainbow .char {
  background: linear-gradient(90deg, #8b5cf6, #ec4899, #f59e0b, #10b981, #22d3ee, #8b5cf6);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: charJump 0.7s cubic-bezier(0.3,1.6,0.5,1) both, rainbowSlide 1.2s linear;
  animation-delay: var(--d), 0s;
}
@keyframes rainbowSlide {
  from { background-position: 0 50%; }
  to { background-position: 300% 50%; }
}

.title .dot {
  display: inline-block;
  background: linear-gradient(120deg, #8b5cf6, #ec4899, #f59e0b);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  position: relative;
  transition: transform 0.3s;
}
.title:hover .dot { transform: scale(1.2) rotate(15deg); }
.title .dot.pop {
  animation: dotPop 0.7s cubic-bezier(0.3,1.6,0.5,1);
}
@keyframes dotPop {
  0% { transform: scale(1); }
  50% { transform: scale(1.6) rotate(-20deg); }
  100% { transform: scale(1); }
}

/* 点击时的水波 ripple */
.ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border-radius: 50%;
  border: 2px solid rgba(139,92,246,0.6);
  pointer-events: none;
  animation: rippleGrow 0.9s ease-out forwards;
}
@keyframes rippleGrow {
  0% { transform: scale(0.3); opacity: 1; }
  100% { transform: scale(10); opacity: 0; }
}
.subtitle {
  font-size: clamp(1rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.7;
  animation: fadeUp 0.8s 0.12s cubic-bezier(0.2,0.8,0.2,1) both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

/* =========================
   Announcement
========================= */
.announce {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 22px;
  margin: 10px 0 40px;
  border-radius: 18px;
  text-decoration: none;
  color: var(--text-primary);
  background: #eef0f4;
  border: 1px solid rgba(15, 23, 42, 0.08);
  box-shadow:
    0 1px 3px rgba(15, 23, 42, 0.06),
    0 6px 20px -8px rgba(15, 23, 42, 0.1);
  transition: transform 0.3s cubic-bezier(0.2,0.8,0.2,1), box-shadow 0.3s, border-color 0.3s;
  animation: fadeUp 0.8s 0.2s cubic-bezier(0.2,0.8,0.2,1) both;
}
html.dark .announce {
  background: rgba(22, 27, 34, 0.7);
  border-color: rgba(120, 140, 180, 0.18);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.25),
    0 6px 20px -12px rgba(0, 0, 0, 0.4);
}
.announce:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: rgba(139,92,246,0.35);
}
.announce-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  background: #0f172a;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
html.dark .announce-icon { background: #fff; color: #0f172a; }
.announce-text { flex: 1; }
.announce-title {
  font-weight: 600;
  font-size: 0.98rem;
  margin-bottom: 2px;
}
.announce-desc {
  color: var(--text-secondary);
  font-size: 0.88rem;
  line-height: 1.5;
}
.announce-arrow {
  color: var(--text-secondary);
  flex-shrink: 0;
  transition: transform 0.3s;
}
.announce:hover .announce-arrow { transform: translateX(4px); }

/* =========================
   Modules grid
========================= */
.modules {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
@media (max-width: 960px) { .modules { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 540px) { .modules { grid-template-columns: 1fr; } }

.card {
  position: relative;
  display: block;
  aspect-ratio: 1 / 1.05;
  min-height: 260px;
  padding: 22px;
  border-radius: 22px;
  background: #e2e5ec;
  border: 1px solid rgba(15, 23, 42, 0.12);
  box-shadow:
    0 1px 3px rgba(15, 23, 42, 0.08),
    0 10px 32px -8px rgba(15, 23, 42, 0.18);
  text-decoration: none;
  color: var(--text-primary);
  overflow: hidden;
  isolation: isolate;
  cursor: pointer;
  transition: transform 0.45s cubic-bezier(0.2,0.8,0.2,1),
              box-shadow 0.45s cubic-bezier(0.2,0.8,0.2,1),
              border-color 0.45s,
              color 0.45s;
  animation: fadeUp 0.6s cubic-bezier(0.2,0.8,0.2,1) both;
}
html.dark .card {
  background: rgba(22, 27, 34, 0.7);
  border-color: rgba(120, 140, 180, 0.18);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.25),
    0 8px 24px -12px rgba(0, 0, 0, 0.4);
}

/* 默认柔色 tint —— 每张卡不同色调,打破纯白 */
.card::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  background:
    radial-gradient(120% 80% at 100% 0%, var(--card-tint-a, rgba(139,92,246,0.22)), transparent 62%),
    radial-gradient(120% 80% at 0% 100%, var(--card-tint-b, rgba(236,72,153,0.18)), transparent 62%);
  opacity: 1;
  transition: opacity 0.45s cubic-bezier(0.2,0.8,0.2,1);
  pointer-events: none;
}
html.dark .card::after { opacity: 0.7; }
.card:hover::after { opacity: 0; }
.card:nth-child(1) { animation-delay: 0.25s; }
.card:nth-child(2) { animation-delay: 0.32s; }
.card:nth-child(3) { animation-delay: 0.39s; }
.card:nth-child(4) { animation-delay: 0.46s; }

.card.inactive {
  cursor: not-allowed;
}

/* hover 时露出的"图片" */
.card-art {
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
  animation: artFloat 8s ease-in-out infinite;
}
.art-a { width: 90%; height: 90%; top: -20%; left: -20%; }
.art-b { width: 80%; height: 80%; top: 15%; right: -25%; animation-delay: -3s; }
.art-c { width: 70%; height: 70%; bottom: -25%; left: 15%; animation-delay: -5s; }
.art-grain {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='1.1' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}

@keyframes artFloat {
  0%,100% { transform: translate(0,0) scale(1); }
  50% { transform: translate(20px,-15px) scale(1.12); }
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 28px 64px -16px rgba(15,23,42,0.3);
  color: #fff;
  border-color: transparent;
}
.card:hover .card-art {
  opacity: 1;
  transform: scale(1);
}
.card:hover .card-desc { color: rgba(255,255,255,0.85); }
.card.inactive:hover .status-dot {
  background: #fff;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.2);
}

.card-inner {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card-top {
  display: flex;
  justify-content: flex-start;
}
.card-icon {
  width: 28px;
  height: 28px;
  color: currentColor;
}
.card-icon :deep(svg) { width: 100%; height: 100%; }

.card-bottom {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.card-title {
  font-size: 1.35rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin: 0;
}
.card-desc {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
  transition: color 0.4s;
}

.status-dot {
  position: absolute;
  top: 16px; right: 16px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #9ca3af;
  box-shadow: 0 0 0 4px rgba(156,163,175,0.15);
  z-index: 2;
}

/* =========================
   Theme palettes (用于 hover 背景 + 默认 tint)
========================= */
.theme-aurora {
  --card-tint-a: rgba(167,139,250,0.32);
  --card-tint-b: rgba(240,171,252,0.26);
}
.theme-aurora .art-a { background: #a78bfa; }
.theme-aurora .art-b { background: #f0abfc; }
.theme-aurora .art-c { background: #60a5fa; }

.theme-citrus {
  --card-tint-a: rgba(253,224,71,0.36);
  --card-tint-b: rgba(251,146,60,0.26);
}
.theme-citrus .art-a { background: #fde047; }
.theme-citrus .art-b { background: #fb923c; }
.theme-citrus .art-c { background: #f472b6; }

.theme-violet {
  --card-tint-a: rgba(129,140,248,0.32);
  --card-tint-b: rgba(34,211,238,0.26);
}
.theme-violet .art-a { background: #818cf8; }
.theme-violet .art-b { background: #22d3ee; }
.theme-violet .art-c { background: #c084fc; }

.theme-sunset {
  --card-tint-a: rgba(252,165,165,0.32);
  --card-tint-b: rgba(253,186,116,0.26);
}
.theme-sunset .art-a { background: #fca5a5; }
.theme-sunset .art-b { background: #fdba74; }
.theme-sunset .art-c { background: #a78bfa; }

/* =========================
   Footer grid
========================= */
.foot-grid {
  position: relative;
  z-index: 1;
  margin-top: 80px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  padding-top: 40px;
  border-top: 1px solid var(--border-color);
}
@media (max-width: 640px) {
  .foot-grid { grid-template-columns: 1fr; gap: 28px; }
}
.foot-head {
  font-size: 0.72rem;
  letter-spacing: 3px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 18px;
}
.foot-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 500;
  border-bottom: 1px solid var(--border-soft);
  transition: color 0.25s, padding 0.25s;
}
.foot-link span {
  color: var(--text-secondary);
  font-size: 0.9rem;
  transition: transform 0.25s;
}
.foot-link:hover {
  color: #8b5cf6;
  padding-left: 4px;
}
.foot-link:hover span { transform: translate(2px, -2px); }
</style>
