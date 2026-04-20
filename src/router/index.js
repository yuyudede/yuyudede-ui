import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
  { path: '/article/:slug', name: 'Article', component: () => import('../views/ArticleView.vue') },
  { path: '/categories', name: 'Categories', component: () => import('../views/CategoryListView.vue') },
  { path: '/category/:slug', name: 'Category', component: () => import('../views/CategoryView.vue') },
  { path: '/tags', name: 'Tags', component: () => import('../views/TagListView.vue') },
  { path: '/tag/:slug', name: 'Tag', component: () => import('../views/TagView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/articles' },
      { path: 'articles', name: 'AdminArticles', component: () => import('../views/admin/ArticleListView.vue') },
      { path: 'articles/new', name: 'AdminArticleNew', component: () => import('../views/admin/ArticleFormView.vue') },
      { path: 'articles/edit/:id', name: 'AdminArticleEdit', component: () => import('../views/admin/ArticleFormView.vue') },
      { path: 'comments', name: 'AdminComments', component: () => import('../views/admin/CommentListView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) {
      return { name: 'Login', query: { redirect: to.fullPath } }
    }
  }
})

export default router
