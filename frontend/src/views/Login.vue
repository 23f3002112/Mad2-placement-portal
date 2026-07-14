<template>
  <div class="login-page-wrapper d-flex flex-grow-1 w-100">
    <div class="row w-100 m-0">
      
      <!-- Left Side: Form -->
      <div class="col-12 col-md-5 d-flex flex-column justify-content-center bg-white px-4 px-md-5 py-5">
        <div class="w-100 mx-auto" style="max-width: 380px;">
          <div class="mb-5">
            <h1 class="fw-bold text-dark mb-2 display-6">Log In</h1>
            <p class="text-muted fs-5">Find the job made for you!</p>
          </div>

          <!-- Social Login Placeholder -->
          <button type="button" @click="handleGoogleLogin" class="btn btn-outline-dark w-100 mb-4 py-2 d-flex align-items-center justify-content-center fw-semibold custom-social-btn">
            <svg class="me-2 google-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path class="g-path-1" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path class="g-path-2" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path class="g-path-3" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path class="g-path-4" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Log In with Google
          </button>

          <div class="d-flex align-items-center mb-4">
            <div class="flex-grow-1 border-bottom"></div>
            <span class="mx-3 text-muted small">or Log In with Email</span>
            <div class="flex-grow-1 border-bottom"></div>
          </div>

          <div v-if="error" class="alert alert-danger py-2 small border-0 rounded-3 text-center">{{ error }}</div>

          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <input type="email" class="form-control form-control-lg custom-input" v-model="email" required placeholder="Email">
            </div>
            <div class="mb-3">
              <input type="password" class="form-control form-control-lg custom-input" v-model="password" required placeholder="Password">
            </div>
            
            <div class="d-flex justify-content-end mb-4">
              <a href="#" class="text-decoration-none small fw-semibold text-dark">Forgot password?</a>
            </div>
            
            <button type="submit" class="btn btn-dark w-100 btn-lg fw-semibold mb-4 custom-btn-login">Log In</button>
            
            <div class="text-center">
              <span class="text-muted small">Not registered? </span>
              <router-link to="/register" class="text-decoration-underline text-dark small fw-semibold custom-link">Create an Account</router-link>
            </div>
          </form>
        </div>
      </div>

      <!-- Right Side: Creative Visuals -->
      <div class="col-md-7 d-none d-md-flex align-items-center justify-content-center position-relative overflow-hidden right-visual">
        <!-- Modern Abstract Art -->
        <div class="shape shape-circle"></div>
        <div class="shape shape-square"></div>
        <div class="shape shape-pill"></div>
        <div class="shape shape-triangle"></div>

        <div class="hero-text position-absolute bottom-0 end-0 p-5 text-end">
          <h1 class="display-4 fw-bold text-dark mb-0">Discover your</h1>
          <h1 class="display-4 fw-bold mb-0" style="color: #00008b;">dream career.</h1>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { googleTokenLogin } from 'vue3-google-login'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

const handleGoogleLogin = () => {
  googleTokenLogin().then((response) => {
    // We send the token to our Flask backend to verify and log the user in
    api.post('/auth/google', { credential: response.access_token })
      .then(res => {
        localStorage.setItem('token', res.data.access_token)
        localStorage.setItem('role', res.data.role)
        router.push(`/${res.data.role}`)
      })
      .catch(err => {
        error.value = err.response?.data?.msg || 'Google Login failed on server.'
      })
  }).catch(err => {
    // User closed the popup or it failed
    console.error("Google login error:", err)
  })
}

const handleLogin = async () => {
  try {
    error.value = ''
    const response = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    })
    
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('role', response.data.role)
    
    router.push(`/${response.data.role}`)
  } catch (err) {
    error.value = err.response?.data?.msg || 'Login failed. Please try again.'
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

.custom-social-btn {
  border-radius: 4px;
  transition: all 0.2s ease;
}

.custom-social-btn:hover {
  background-color: #00008b;
  color: #ffffff !important;
  border-color: #00008b;
}

.custom-social-btn:hover .google-icon path {
  fill: #ffffff; /* Make google logo white on hover */
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

/* Right Side Creative Art */
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
