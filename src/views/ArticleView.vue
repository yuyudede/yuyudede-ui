<template>
  <div class="article-page">
    <div class="article-layout" v-loading="loading">
      <!-- TOC 侧边栏 -->
      <aside v-if="tocItems.length > 0" class="toc-sidebar">
        <div class="toc-card glass-card">
          <h4 class="toc-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
            目录
          </h4>
          <nav class="toc-nav">
            <a
              v-for="item in tocItems"
              :key="item.id"
              :href="`#${item.id}`"
              :class="['toc-link', `toc-h${item.level}`, { active: activeId === item.id }]"
              @click.prevent="scrollToHeading(item.id)"
            >
              {{ item.text }}
            </a>
          </nav>
        </div>
      </aside>

      <!-- 文章主体 -->
      <div class="article-main">
        <article v-if="article" class="article-detail glass-container">
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <span class="meta-date">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <path d="M16 2v4M8 2v4M3 10h18"/>
              </svg>
              {{ formatDate(article.createdAt) }}
            </span>
            <span v-if="article.readingMinutes" class="meta-reading">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
              {{ article.readingMinutes }} 分钟阅读
            </span>
            <router-link
              v-if="article.category"
              :to="`/category/${article.category.slug}`"
              class="meta-category"
            >
              <el-tag type="primary" size="small">{{ article.category.name }}</el-tag>
            </router-link>
            <div class="meta-tags">
              <router-link
                v-for="tag in article.tagNames"
                :key="tag"
                :to="`/tag/${tag}`"
                class="tag-link"
              >
                <el-tag size="small" type="info" effect="plain">{{ tag }}</el-tag>
              </router-link>
            </div>
          </div>
          <div class="divider"></div>
          <div ref="contentRef" class="article-content" v-html="article.contentHtml"></div>
        </article>

        <section v-if="article" class="comments-section glass-container">
          <h3 class="comments-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            评论 ({{ comments.length }})
          </h3>
          <div class="comment-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-avatar">
                <span>{{ comment.nickname ? comment.nickname[0].toUpperCase() : '?' }}</span>
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <strong class="comment-name">{{ comment.nickname }}</strong>
                  <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
                </div>
                <p class="comment-content">{{ comment.content }}</p>
              </div>
            </div>
            <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧！" :image-size="80" />
          </div>

          <div class="comment-form glass-form">
            <h4 class="form-title">发表评论</h4>
            <el-form
              ref="formRef"
              :model="commentForm"
              :rules="commentRules"
              label-width="60px"
              @submit.prevent="submitComment"
            >
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="commentForm.nickname" placeholder="请输入昵称" />
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="commentForm.email" placeholder="请输入邮箱" />
              </el-form-item>
              <el-form-item label="内容" prop="content">
                <el-input
                  v-model="commentForm.content"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入评论内容"
                />
              </el-form-item>
              <el-form-item>
                <button type="submit" :disabled="submitting" class="submit-btn">
                  <span v-if="submitting">提交中...</span>
                  <span v-else>提交评论</span>
                </button>
              </el-form-item>
            </el-form>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import { ElMessage } from 'element-plus'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import api from '../api'

const route = useRoute()
const article = ref(null)
const comments = ref([])
const loading = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const contentRef = ref(null)
const tocItems = ref([])
const activeId = ref('')

const commentForm = ref({
  nickname: '',
  email: '',
  content: '',
})

const commentRules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  content: [{ required: true, message: '请输入评论内容', trigger: 'blur' }],
}

// SEO head
useHead({
  title: () => article.value ? `${article.value.title} - yuyudede` : 'yuyudede',
  meta: () => {
    if (!article.value) return []
    return [
      { name: 'description', content: article.value.summary || article.value.title },
      { property: 'og:title', content: article.value.title },
      { property: 'og:description', content: article.value.summary || '' },
      { property: 'og:type', content: 'article' },
      { property: 'og:url', content: `https://yuyudede.com/article/${article.value.slug}` },
    ]
  },
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

async function fetchArticle() {
  loading.value = true
  try {
    const { data } = await api.get(`/articles/${route.params.slug}`)
    article.value = data
    await nextTick()
    highlightCode()
    extractToc()
    observeHeadings()
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  const { data } = await api.get(`/articles/${route.params.slug}/comments`)
  comments.value = data
}

function highlightCode() {
  if (!contentRef.value) return
  const blocks = contentRef.value.querySelectorAll('pre code')
  blocks.forEach((block) => {
    hljs.highlightElement(block)
    // 添加复制按钮
    const pre = block.parentElement
    if (pre.querySelector('.copy-btn')) return
    pre.style.position = 'relative'
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.textContent = '复制'
    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(block.textContent).then(() => {
        btn.textContent = '已复制'
        btn.classList.add('copied')
        setTimeout(() => {
          btn.textContent = '复制'
          btn.classList.remove('copied')
        }, 2000)
      })
    })
    pre.appendChild(btn)
  })
}

function extractToc() {
  if (!contentRef.value) return
  const headings = contentRef.value.querySelectorAll('h1, h2, h3')
  tocItems.value = Array.from(headings).map((h) => ({
    id: h.id || h.textContent.trim().toLowerCase().replace(/\s+/g, '-'),
    text: h.textContent.trim(),
    level: parseInt(h.tagName[1]),
  }))
  // 确保每个标题都有 id
  headings.forEach((h, i) => {
    if (!h.id) {
      h.id = tocItems.value[i].id
    }
  })
}

let observer = null
function observeHeadings() {
  if (observer) observer.disconnect()
  if (!contentRef.value) return
  const headings = contentRef.value.querySelectorAll('h1[id], h2[id], h3[id]')
  if (headings.length === 0) return

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeId.value = entry.target.id
          break
        }
      }
    },
    { rootMargin: '-80px 0px -60% 0px', threshold: 0 }
  )
  headings.forEach((h) => observer.observe(h))
}

function scrollToHeading(id) {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeId.value = id
  }
}

async function submitComment() {
  if (!formRef.value) return
  await formRef.value.validate()
  submitting.value = true
  try {
    await api.post(`/articles/${route.params.slug}/comments`, commentForm.value)
    ElMessage.success('评论提交成功，等待审核')
    commentForm.value = { nickname: '', email: '', content: '' }
    formRef.value.resetFields()
    fetchComments()
  } catch {
    ElMessage.error('评论提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchArticle()
  fetchComments()
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.article-page {
  padding: 32px 0;
}

.article-layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.article-main {
  flex: 1;
  max-width: 800px;
  min-width: 0;
}

/* TOC 侧边栏 */
.toc-sidebar {
  width: 220px;
  flex-shrink: 0;
  position: sticky;
  top: 84px;
  order: 1;
}
.toc-card {
  padding: 16px;
  border-radius: 16px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  box-shadow: var(--glass-shadow);
}
.toc-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 10px;
}
.toc-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-height: calc(100vh - 180px);
  overflow-y: auto;
}
.toc-link {
  font-size: 0.82rem;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 6px;
  border-left: 2px solid transparent;
  transition: all 0.2s;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.toc-link:hover {
  color: var(--primary);
}
.toc-link.active {
  color: var(--primary);
  border-left-color: var(--primary);
  background: rgba(129, 140, 248, 0.08);
}
.toc-h2 { padding-left: 8px; }
.toc-h3 { padding-left: 20px; font-size: 0.78rem; }

/* 磨砂容器 */
.glass-container {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  border-radius: 20px;
  padding: 32px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 24px;
}

.article-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.35;
  letter-spacing: -0.02em;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.meta-date, .meta-reading {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.meta-category {
  text-decoration: none;
}

.meta-tags {
  display: flex;
  gap: 6px;
}

.tag-link {
  text-decoration: none;
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
  margin: 20px 0;
}

.article-content {
  line-height: 2;
  font-size: 1.05rem;
  color: var(--text-primary);
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin-top: 40px;
  margin-bottom: 16px;
  line-height: 1.4;
  letter-spacing: -0.01em;
}
.article-content :deep(h1) {
  font-size: 1.6rem;
  font-weight: 700;
}
.article-content :deep(h2) {
  font-size: 1.35rem;
  font-weight: 650;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-soft);
}
.article-content :deep(h3) {
  font-size: 1.15rem;
  font-weight: 600;
}

.article-content :deep(p) {
  margin-bottom: 20px;
}

.article-content :deep(pre) {
  background: var(--code-bg);
  padding: 20px;
  border-radius: 14px;
  overflow-x: auto;
  border: 1px solid var(--border-soft);
  position: relative;
  margin: 20px 0;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.03);
}

.article-content :deep(code) {
  font-family: 'Fira Code', 'SF Mono', 'Cascadia Code', monospace;
  font-size: 0.88em;
}

/* 行间代码 */
.article-content :deep(:not(pre) > code) {
  background: var(--code-bg);
  padding: 2px 8px;
  border-radius: 6px;
  color: #ec4899;
  font-size: 0.88em;
  border: 1px solid var(--border-soft);
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 14px;
  margin: 24px 0;
  box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.12);
  border: 1px solid var(--border-soft);
}

.article-content :deep(blockquote) {
  background: rgba(129, 140, 248, 0.06);
  border-left: 4px solid var(--primary);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  color: var(--text-secondary);
  margin: 20px 0;
  font-style: italic;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  padding-left: 24px;
  margin: 16px 0;
}
.article-content :deep(li) {
  margin-bottom: 8px;
}

.article-content :deep(hr) {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
  margin: 32px 0;
}

/* 复制按钮 */
.article-content :deep(.copy-btn) {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 12px;
  font-size: 0.72rem;
  color: var(--text-secondary);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(4px);
  z-index: 1;
}
.article-content :deep(.copy-btn:hover) {
  color: #fff;
  background: rgba(129, 140, 248, 0.6);
  border-color: rgba(129, 140, 248, 0.6);
}
.article-content :deep(.copy-btn.copied) {
  color: #10b981;
  border-color: #10b981;
}

/* 评论区 */
.comments-section {
  padding: 32px;
}

.comments-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.15rem;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.comment-item {
  display: flex;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-soft);
}
.comment-item:last-child {
  border-bottom: none;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 2px 8px -2px rgba(129, 140, 248, 0.4);
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-name {
  font-size: 0.92rem;
  color: var(--text-primary);
  font-weight: 600;
}

.comment-date {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.comment-content {
  color: var(--text-secondary);
  line-height: 1.7;
  font-size: 0.92rem;
}

/* 评论表单 */
.glass-form {
  margin-top: 28px;
  padding: 28px;
  border-radius: 18px;
  background: rgba(129, 140, 248, 0.04);
  border: 1px solid var(--glass-border);
}

.form-title {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.submit-btn {
  padding: 10px 28px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s, opacity 0.25s;
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(129, 140, 248, 0.5);
}
.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .toc-sidebar {
    display: none;
  }
  .article-layout {
    max-width: 800px;
  }
}

@media (max-width: 640px) {
  .glass-container {
    padding: 24px 20px;
    border-radius: 16px;
  }
  .article-title {
    font-size: 1.7rem;
  }
  .article-content {
    font-size: 1rem;
    line-height: 1.85;
  }
  .comment-item {
    gap: 10px;
  }
  .comment-avatar {
    width: 34px;
    height: 34px;
    font-size: 0.85rem;
  }
  .glass-form {
    padding: 20px;
  }
}
</style>
