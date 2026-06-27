<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-6 col-lg-4">
      <div class="card shadow border-0 rounded-lg">
        <div class="card-body p-4">
          <h3 class="text-center mb-4 fw-bold">Welcome Back</h3>
          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label text-muted">Email address</label>
              <input type="email" class="form-control form-control-lg bg-light" v-model="email" required placeholder="name@example.com">
            </div>
            <div class="mb-4">
              <label class="form-label text-muted">Password</label>
              <input type="password" class="form-control form-control-lg bg-light" v-model="password" required placeholder="••••••••">
            </div>
            <button type="submit" class="btn btn-primary w-100 btn-lg mb-3">Login</button>
            <div class="text-center">
              <span class="text-muted">Don't have an account? </span>
              <router-link to="/register" class="text-decoration-none fw-semibold">Register here</router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    error.value = ''
    const response = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    })
    
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('role', response.data.role)
    
    // Redirect based on role
    router.push(`/${response.data.role}`)
  } catch (err) {
    error.value = err.response?.data?.msg || 'Login failed. Please try again.'
  }
}
</script>
