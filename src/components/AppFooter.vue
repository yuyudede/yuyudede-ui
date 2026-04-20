<template>
  <el-footer class="footer">
    <p>&copy; {{ year }} yuyudede. All rights reserved.</p>
  </el-footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  text-align: center;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>
