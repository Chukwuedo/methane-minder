<template>
  <div class="flex flex-col min-h-screen max-w-screen-xl bg-base-200 " :data-theme="theme">
    <Dashboard @toggle-theme="toggleTheme" :theme="theme" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'

const theme = ref('accenture-dark')

function toggleTheme() {
  theme.value = theme.value === 'accenture-dark' ? 'accenture-light' : 'accenture-dark'
}
</script>
