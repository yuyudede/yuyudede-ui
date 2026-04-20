<template>
  <div class="article-form-page">
    <h3>{{ isEdit ? '编辑文章' : '新建文章' }}</h3>
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      v-loading="loading"
    >
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入文章标题" @blur="generateSlug" />
      </el-form-item>
      <el-form-item label="Slug" prop="slug">
        <el-input v-model="form.slug" placeholder="URL 友好的标识，留空自动生成" />
      </el-form-item>
      <el-form-item label="分类" prop="categoryId">
        <el-select v-model="form.categoryId" placeholder="请选择分类" clearable>
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="cat.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="标签" prop="tagNames">
        <el-input v-model="tagInput" placeholder="多个标签用英文逗号分隔" />
      </el-form-item>
      <el-form-item label="摘要" prop="summary">
        <el-input
          v-model="form.summary"
          type="textarea"
          :rows="3"
          placeholder="请输入文章摘要"
        />
      </el-form-item>
      <el-form-item label="正文" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="15"
          placeholder="请输入 Markdown 格式的文章正文"
        />
      </el-form-item>
      <el-form-item label="发布">
        <el-switch v-model="form.published" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="saving" @click="handleSave">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../../api'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const categories = ref([])
const tagInput = ref('')

const isEdit = computed(() => !!route.params.id)

const form = ref({
  title: '',
  slug: '',
  categoryId: null,
  summary: '',
  content: '',
  published: false,
})

const rules = {
  title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入文章正文', trigger: 'blur' }],
}

function generateSlug() {
  if (!form.value.slug && form.value.title) {
    form.value.slug = form.value.title
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
      .replace(/^-|-$/g, '')
  }
}

async function fetchCategories() {
  const { data } = await api.get('/categories')
  categories.value = data
}

async function fetchArticle() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const { data } = await api.get(`/admin/articles/${route.params.id}`)
    form.value = {
      title: data.title,
      slug: data.slug,
      categoryId: data.category?.id || null,
      summary: data.summary || '',
      content: data.content,
      published: data.published,
    }
    tagInput.value = (data.tagNames || []).join(', ')
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!formRef.value) return
  await formRef.value.validate()
  saving.value = true

  const payload = {
    ...form.value,
    tagNames: tagInput.value
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean),
  }

  try {
    if (isEdit.value) {
      await api.put(`/admin/articles/${route.params.id}`, payload)
      ElMessage.success('文章更新成功')
    } else {
      await api.post('/admin/articles', payload)
      ElMessage.success('文章创建成功')
    }
    router.push('/admin/articles')
  } catch {
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchArticle()
})
</script>

<style scoped>
.article-form-page {
  max-width: 800px;
}

.article-form-page h3 {
  margin-bottom: 24px;
}
</style>
