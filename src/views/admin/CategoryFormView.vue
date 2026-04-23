<template>
  <div class="category-form-page">
    <h3>{{ isEdit ? '编辑分类' : '新建分类' }}</h3>
    <div class="form-card glass-card">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" @blur="generateSlug" />
        </el-form-item>
        <el-form-item label="Slug" prop="slug">
          <el-input v-model="form.slug" placeholder="URL 友好的标识，留空自动生成" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分类描述（可选）"
          />
        </el-form-item>
        <el-form-item>
          <button type="button" class="btn-primary" :disabled="saving" @click="handleSave">
            <span v-if="saving">保存中...</span>
            <span v-else>{{ isEdit ? '更新' : '创建' }}</span>
          </button>
          <button type="button" class="btn-secondary" @click="$router.back()">取消</button>
        </el-form-item>
      </el-form>
    </div>
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
const saving = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = ref({
  name: '',
  slug: '',
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
}

function generateSlug() {
  if (!form.value.slug && form.value.name) {
    form.value.slug = form.value.name
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
      .replace(/^-|-$/g, '')
  }
}

async function fetchCategory() {
  if (!isEdit.value) return
  try {
    const { data } = await api.get(`/admin/categories`)
    const cat = data.find(c => c.id === Number(route.params.id))
    if (cat) {
      form.value = {
        name: cat.name,
        slug: cat.slug,
        description: cat.description || '',
      }
    }
  } catch {
    ElMessage.error('获取分类信息失败')
  }
}

async function handleSave() {
  if (!formRef.value) return
  await formRef.value.validate()
  saving.value = true

  try {
    if (isEdit.value) {
      await api.put(`/admin/categories/${route.params.id}`, form.value)
      ElMessage.success('分类更新成功')
    } else {
      await api.post('/admin/categories', form.value)
      ElMessage.success('分类创建成功')
    }
    router.push('/admin/categories')
  } catch {
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    saving.value = false
  }
}

onMounted(fetchCategory)
</script>

<style scoped>
.category-form-page {
  max-width: 600px;
}
.category-form-page h3 {
  margin-bottom: 20px;
  font-size: 1.15rem;
  font-weight: 600;
}

.form-card {
  padding: 28px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur) var(--glass-saturate);
  -webkit-backdrop-filter: var(--glass-blur) var(--glass-saturate);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  padding: 0 20px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s, opacity 0.25s;
  margin-right: 10px;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(129, 140, 248, 0.5);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  height: 38px;
  padding: 0 20px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary:hover {
  border-color: var(--primary);
  color: var(--primary);
}
</style>
