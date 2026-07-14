<template>
  <div class="login-page-wrapper d-flex flex-grow-1 w-100">
    <div class="row w-100 m-0">

      <!-- Left Side: Creative Visuals -->
      <div class="col-md-7 d-none d-md-flex align-items-center justify-content-center position-relative overflow-hidden right-visual">
        <!-- Modern Abstract Art -->
        <div class="shape shape-circle"></div>
        <div class="shape shape-square"></div>
        <div class="shape shape-pill"></div>
        <div class="shape shape-triangle"></div>

        <div class="hero-text position-absolute bottom-0 start-0 p-5 text-start">
          <h1 class="display-4 fw-bold text-dark mb-0">Start your</h1>
          <h1 class="display-4 fw-bold mb-0" style="color: #00008b;">journey today.</h1>
        </div>
      </div>
      
      <!-- Right Side: Form -->
      <div class="col-12 col-md-5 d-flex flex-column justify-content-center bg-white px-4 px-md-5 py-5">
        <div class="w-100 mx-auto" style="max-width: 380px;">
          <div class="mb-5">
            <h1 class="fw-bold text-dark mb-2 display-6">Register</h1>
            <p class="text-muted fs-5">Create an account to continue</p>
          </div>
          
          <ul class="nav nav-pills nav-fill mb-4 custom-pills">
            <li class="nav-item">
              <a class="nav-link fw-semibold rounded-3" :class="{ active: role === 'student' }" @click="role = 'student'" href="#">Student</a>
            </li>
            <li class="nav-item">
              <a class="nav-link fw-semibold rounded-3" :class="{ active: role === 'company' }" @click="role = 'company'" href="#">Company</a>
            </li>
          </ul>

          <div v-if="error" class="alert alert-danger py-2 small border-0 rounded-3 text-center">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2 small border-0 rounded-3 text-center">{{ success }}</div>

          <form @submit.prevent="handleRegister">
            <div class="mb-3" v-if="role === 'student'">
              <input type="text" class="form-control form-control-lg custom-input" v-model="form.name" required placeholder="Full Name">
            </div>
            
            <div class="mb-3" v-if="role === 'company'">
              <input type="text" class="form-control form-control-lg custom-input" v-model="form.company_name" required placeholder="Company Name">
            </div>

            <div class="mb-3">
              <input type="email" class="form-control form-control-lg custom-input" v-model="form.email" required placeholder="Email Address">
            </div>
            
            <div class="mb-4">
              <input type="password" class="form-control form-control-lg custom-input" v-model="form.password" required placeholder="Password">
            </div>
            
            <button type="submit" class="btn btn-dark w-100 btn-lg fw-semibold mb-4 custom-btn-login">Create Account</button>
            
            <div class="text-center">
              <span class="text-muted small">Already have an account? </span>
              <router-link to="/login" class="text-decoration-underline text-dark small fw-semibold custom-link">Log In</router-link>
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
.login-page-wrapper {
  margin: -1.5rem 0; /* Negate the container margins to go full width */
}

/* Form Styles */
.custom-input {
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.95rem;
  padding: 0.75rem 1rem;
}

.custom-input:focus {
  border-color: #00008b;
  box-shadow: 0 0 0 3px rgba(0, 0, 139, 0.1);
}

.custom-btn-login {
  background-color: #000;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.custom-btn-login:hover {
  background-color: #00008b;
  box-shadow: 0 4px 12px rgba(0, 0, 139, 0.3);
}

.custom-link:hover {
  color: #ff3e6c !important;
}

/* Pills */
.custom-pills .nav-link {
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s ease;
}
.custom-pills .nav-link.active {
  background-color: #00008b;
  color: white;
}

/* Creative Art */
.right-visual {
  background-color: #f4f6f8;
  min-height: calc(100vh - 80px);
}

.shape {
  position: absolute;
  animation: float 8s ease-in-out infinite alternate;
}

.shape-circle {
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00008b, #4a4aef);
  top: 10%;
  left: 20%;
}

.shape-square {
  width: 150px;
  height: 150px;
  background-color: #ff3e6c;
  border-radius: 20px;
  top: 40%;
  right: 15%;
  transform: rotate(15deg);
  animation-delay: -2s;
}

.shape-pill {
  width: 200px;
  height: 80px;
  background-color: #ffd700;
  border-radius: 40px;
  bottom: 25%;
  left: 15%;
  transform: rotate(-20deg);
  animation-delay: -4s;
}

.shape-triangle {
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-bottom: 104px solid #00d2ff;
  top: 20%;
  right: 30%;
  transform: rotate(45deg);
  animation-delay: -6s;
}

@keyframes float {
  0% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
  100% { transform: translateY(10px) rotate(-5deg); }
}

.hero-text {
  z-index: 20;
}
</style>
