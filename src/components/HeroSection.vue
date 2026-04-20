<template>
  <section class="hero">
    <div class="hero-content">
      <h1 class="typewriter">Welcome to yuyudede's Blog</h1>
      <p class="subtitle">记录技术 · 分享生活</p>
    </div>
    <div class="wave">
      <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
        <path
          d="M0,64 C360,120 720,0 1080,64 C1260,96 1380,80 1440,64 L1440,120 L0,120 Z"
          fill="#f5f7fa"
        />
      </svg>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background: var(--bg-hero);
  position: relative;
  padding: 100px 20px 80px;
  text-align: center;
  color: #fff;
  overflow: hidden;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 700;
  display: inline-block;
}

.subtitle {
  margin-top: 20px;
  font-size: 1.2rem;
  opacity: 0.9;
  letter-spacing: 2px;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  line-height: 0;
}

.wave svg {
  width: 100%;
  height: 60px;
}
</style>
