<!-- src/App.vue -->
<template>
  <div id="app">
    <GeneratorView />
  </div>
</template>

<script setup>
import GeneratorView from './views/GeneratorView.vue'
</script>

<style>
/* 全局重置（可选） */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f9fafb;
  color: #1f2937;
}
</style>