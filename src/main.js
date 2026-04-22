import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import App from './App.vue'
import router from './router'
import './styles/global.css'

const app = createApp(App)
const head = createHead()
app.use(createPinia())
app.use(router)
app.use(head)
app.use(ElementPlus)
app.mount('#app')
