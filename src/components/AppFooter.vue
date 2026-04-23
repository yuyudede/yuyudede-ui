<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="brand-dot"></span>
        <span class="brand-name">yuyudede</span>
      </div>

      <div class="footer-grid">
        <div class="footer-col">
          <div class="col-head">EXPLORE</div>
          <router-link to="/blog" class="col-link">博客</router-link>
          <router-link to="/categories" class="col-link">分类</router-link>
          <router-link to="/tags" class="col-link">标签</router-link>
        </div>
        <div class="footer-col">
          <div class="col-head">CONNECT</div>
          <a href="#" class="col-link" target="_blank" rel="noopener">GitHub</a>
          <a href="#" class="col-link" target="_blank" rel="noopener">Email</a>
          <a href="#" class="col-link" target="_blank" rel="noopener">RSS</a>
        </div>
        <div class="footer-col">
          <div class="col-head">ABOUT</div>
          <a href="#" class="col-link">关于我</a>
          <a href="#" class="col-link">友链</a>
          <a href="#" class="col-link">留言板</a>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="copyright">&copy; {{ year }} yuyudede. All rights reserved.</p>
        <p class="made-with">Crafted with Vue & Passion</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  position: relative;
  border-top: 1px solid var(--border-color);
  background: var(--bg-surface);
}

.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 20px 32px;
}

.footer-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 36px;
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

.footer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  max-width: 600px;
  margin: 0 auto 36px;
  text-align: center;
}

@media (max-width: 640px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

.col-head {
  font-size: 0.72rem;
  letter-spacing: 3px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 14px;
}
.col-link {
  display: block;
  padding: 6px 0;
  color: var(--text-primary);
  text-decoration: none;
  font-size: 0.92rem;
  transition: color 0.25s, transform 0.25s;
}
.col-link:hover {
  color: #8b5cf6;
  transform: translateX(2px);
}

.footer-bottom {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid var(--border-soft);
}
.copyright {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 4px;
}
.made-with {
  color: var(--text-secondary);
  font-size: 0.75rem;
  opacity: 0.7;
}
</style>
