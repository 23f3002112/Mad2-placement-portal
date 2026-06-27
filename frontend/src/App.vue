<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4 shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#">🎓 Placement Portal V2</a>
        <div class="navbar-nav ms-auto" v-if="isLoggedIn">
          <button @click="logout" class="btn btn-outline-light btn-sm">Logout</button>
        </div>
      </div>
    </nav>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Force reactivity based on route changes is tricky with just localStorage,
// but for milestone 2 basic auth, this is a reasonable start. 
// We will improve this when we add Pinia later.
const isLoggedIn = computed(() => {
  // A simple hack to make it reactive without Pinia for now
  router.currentRoute.value;
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<style>
body {
  background-color: #f8f9fa;
}
</style>
