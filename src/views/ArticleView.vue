<template>
  <div class="article-page">
    <div class="container" v-loading="loading">
      <article v-if="article" class="article-detail">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="meta-date">{{ formatDate(article.createdAt) }}</span>
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
        <el-divider />
        <div class="article-content" v-html="article.contentHtml"></div>
      </article>

      <el-divider v-if="article" />

      <section v-if="article" class="comments-section">
        <h3>评论 ({{ comments.length }})</h3>
        <div class="comment-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <strong>{{ comment.nickname }}</strong>
              <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
          <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧！" :image-size="80" />
        </div>

        <el-card class="comment-form-card" shadow="never">
          <h4>发表评论</h4>
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
              <el-button type="primary" :loading="submitting" @click="submitComment">
                提交评论
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const route = useRoute()
const article = ref(null)
const comments = ref([])
const loading = ref(false)
const submitting = ref(false)
const formRef = ref(null)

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

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

async function fetchArticle() {
  loading.value = true
  try {
    const { data } = await api.get(`/articles/${route.params.slug}`)
    article.value = data
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  const { data } = await api.get(`/articles/${route.params.slug}/comments`)
  comments.value = data
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
</script>

<style scoped>
.article-page {
  padding: 32px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  min-height: 400px;
}

.article-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.4;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--text-secondary);
  font-size: 0.9rem;
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

.article-content {
  line-height: 1.8;
  font-size: 1rem;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin-top: 24px;
  margin-bottom: 12px;
}

.article-content :deep(pre) {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.article-content :deep(code) {
  font-family: 'Fira Code', monospace;
  font-size: 0.9em;
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.article-content :deep(blockquote) {
  border-left: 4px solid var(--primary);
  padding-left: 16px;
  color: var(--text-secondary);
  margin: 16px 0;
}

.comments-section h3 {
  margin-bottom: 20px;
}

.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid var(--border-soft);
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-date {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.comment-content {
  color: var(--text-primary);
  line-height: 1.6;
}

.comment-form-card {
  margin-top: 24px;
}

.comment-form-card h4 {
  margin-bottom: 16px;
}
</style>
