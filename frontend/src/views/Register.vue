<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-8 col-lg-6">
      <div class="card shadow border-0 rounded-lg">
        <div class="card-body p-4">
          <h3 class="text-center mb-4 fw-bold">Create an Account</h3>
          
          <ul class="nav nav-pills nav-fill mb-4 custom-pills">
            <li class="nav-item">
              <a class="nav-link" :class="{ active: role === 'student' }" @click="role = 'student'" href="#">Student</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" :class="{ active: role === 'company' }" @click="role = 'company'" href="#">Company</a>
            </li>
          </ul>

          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2">{{ success }}</div>

          <form @submit.prevent="handleRegister">
            <div class="mb-3" v-if="role === 'student'">
              <label class="form-label text-muted">Full Name</label>
              <input type="text" class="form-control bg-light" v-model="form.name" required>
            </div>
            
            <div class="mb-3" v-if="role === 'company'">
              <label class="form-label text-muted">Company Name</label>
              <input type="text" class="form-control bg-light" v-model="form.company_name" required>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted">Email address</label>
              <input type="email" class="form-control bg-light" v-model="form.email" required>
            </div>
            
            <div class="mb-4">
              <label class="form-label text-muted">Password</label>
              <input type="password" class="form-control bg-light" v-model="form.password" required>
            </div>
            
            <button type="submit" class="btn btn-primary w-100 btn-lg mb-3">Register</button>
            <div class="text-center">
              <span class="text-muted">Already have an account? </span>
              <router-link to="/login" class="text-decoration-none fw-semibold">Login here</router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import api from '../services/api'

const role = ref('student')
const error = ref('')
const success = ref('')

const form = reactive({
  name: '',
  company_name: '',
  email: '',
  password: ''
})

const handleRegister = async () => {
  try {
    error.value = ''
    success.value = ''
    
    const endpoint = role.value === 'student' ? '/auth/register/student' : '/auth/register/company'
    const payload = {
      email: form.email,
      password: form.password,
      ...(role.value === 'student' ? { name: form.name } : { company_name: form.company_name })
    }
    
    const response = await api.post(endpoint, payload)
    success.value = response.data.msg
    
    // Reset form
    form.name = ''
    form.company_name = ''
    form.email = ''
    form.password = ''
  } catch (err) {
    error.value = err.response?.data?.msg || 'Registration failed.'
  }
}
</script>

<style scoped>
.custom-pills .nav-link {
  color: #6c757d;
  cursor: pointer;
}
.custom-pills .nav-link.active {
  background-color: #0d6efd;
  color: white;
}
</style>
