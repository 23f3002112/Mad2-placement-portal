<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom py-3">
      <div class="container-fluid px-4 px-lg-5">
        <router-link class="navbar-brand fw-bold fs-3" to="/">
          <span class="text-dark tracking-tight">Job</span><span style="color: #ff3e6c;">Finder</span>
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4" v-if="!isLoggedIn">
            <li class="nav-item">
              <a class="nav-link text-dark fw-medium mx-2" href="#">Discover</a>
            </li>
            <li class="nav-item">
              <a class="nav-link text-dark fw-medium mx-2" href="#">For job seekers</a>
            </li>
            <li class="nav-item">
              <a class="nav-link text-dark fw-medium mx-2" href="#">For companies</a>
            </li>
          </ul>
          
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4" v-else>
            <!-- Spacer for logged in users -->
          </ul>

          <div class="navbar-nav ms-auto align-items-center" v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link fw-medium px-4 py-2 me-2 nav-btn-login">Log In</router-link>
            <router-link to="/register" class="btn rounded-pill fw-medium px-4 py-2 nav-btn-signup">Sign Up</router-link>
          </div>
          <div class="navbar-nav ms-auto align-items-center flex-row gap-4" v-else>
            <!-- Search Bar -->
            <form class="position-relative me-2" @submit.prevent="handleSearch">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="position-absolute text-muted" style="left: 12px; top: 50%; transform: translateY(-50%);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input type="text" v-model="globalSearch" class="form-control rounded-pill border-0 bg-light ps-5 pe-3 py-2" placeholder="Search everywhere..." style="width: 240px; font-size: 0.95rem;">
            </form>
            
            <!-- Notification Bell Dropdown -->
            <div class="nav-item dropdown">
              <a class="nav-link dropdown-toggle d-flex align-items-center text-secondary position-relative custom-nav-icon hide-caret" href="#" id="notificationDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
                <span v-if="unreadCount > 0" class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle" style="margin-top: 4px; margin-left: -4px;">
                  <span class="visually-hidden">New notifications</span>
                </span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-3 rounded-3 p-0" aria-labelledby="notificationDropdown" style="width: 320px;">
                <li class="p-3 border-bottom d-flex justify-content-between align-items-center">
                  <h6 class="mb-0 fw-bold">Notifications</h6>
                  <span class="badge bg-primary rounded-pill" v-if="unreadCount > 0">{{ unreadCount }} New</span>
                </li>
                <div class="overflow-auto custom-scrollbar" style="max-height: 320px;">
                  <li v-for="notif in notifications" :key="notif.id" class="border-bottom" :class="{'bg-light': !notif.is_read}">
                    <a class="dropdown-item py-3 text-wrap" href="#" @click.prevent="markAsRead(notif.id)">
                      <div class="d-flex justify-content-between align-items-start mb-1">
                        <strong class="text-dark d-block" style="font-size: 0.9rem;">{{ notif.title }}</strong>
                        <small class="text-muted ms-2" style="font-size: 0.75rem;">{{ new Date(notif.created_at).toLocaleDateString() }}</small>
                      </div>
                      <span class="d-block text-muted" style="font-size: 0.85rem; line-height: 1.4;">{{ notif.message }}</span>
                    </a>
                  </li>
                  <li v-if="notifications.length === 0" class="p-5 text-center text-muted">
                    No new notifications.
                  </li>
                </div>
              </ul>
            </div>

            <!-- Profile Dropdown -->
            <div class="nav-item dropdown ms-2">
              <a class="nav-link dropdown-toggle d-flex align-items-center text-dark hide-caret" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <div class="rounded-circle bg-light d-flex align-items-center justify-content-center text-secondary border border-2 profile-avatar transition-all">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                </div>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ms-2 text-muted"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </a>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-3 rounded-3" aria-labelledby="navbarDropdownMenuLink" style="min-width: 200px;">
                <li><h6 class="dropdown-header text-muted fw-semibold">My Account</h6></li>
                <li><router-link :to="`/${userRole}`" class="dropdown-item py-2 fw-medium"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg> Dashboard</router-link></li>
                <li v-if="userRole !== 'admin'"><router-link :to="`/${userRole}/profile`" class="dropdown-item py-2 fw-medium"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg> Profile</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><button @click="logout" class="dropdown-item py-2 text-danger fw-medium"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg> Logout</button></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Use container only if not on the landing page -->
    <div :class="{'container mt-4 flex-grow-1': $route.path !== '/', 'flex-grow-1': $route.path === '/'}">
      <router-view></router-view>
    </div>

    <!-- Footer -->
    <footer class="app-footer mt-5">
      <div class="container py-5">
        <div class="row gy-4">
          <div class="col-lg-3 col-md-6">
            <router-link class="navbar-brand fw-bold fs-3 text-white text-decoration-none" to="/">
              <span class="tracking-tight">Job</span><span class="text-primary">Finder</span>
            </router-link>
            <p class="text-secondary mt-3 mb-0" style="font-size: 0.9rem; color: #a9a2b1 !important;">
              Connecting top talent with the best opportunities.
            </p>
          </div>
          <div class="col-lg-3 col-md-6">
            <h5 class="text-white mb-3 fw-semibold">For Students</h5>
            <ul class="list-unstyled footer-links">
              <li><router-link to="/login">Student Login</router-link></li>
              <li><router-link to="/register?role=student">Create Profile</router-link></li>
              <li><router-link to="/student/jobs">Browse Jobs</router-link></li>
              <li><router-link to="/student/applications">Track Applications</router-link></li>
            </ul>
          </div>
          <div class="col-lg-3 col-md-6">
            <h5 class="text-white mb-3 fw-semibold">For Companies</h5>
            <ul class="list-unstyled footer-links">
              <li><router-link to="/login">Company Login</router-link></li>
              <li><router-link to="/register?role=company">Register Company</router-link></li>
              <li><router-link to="/company/jobs">Manage Jobs</router-link></li>
              <li><router-link to="/company/applications">Review Applicants</router-link></li>
            </ul>
          </div>
          <div class="col-lg-3 col-md-6">
            <h5 class="text-white mb-3 fw-semibold">Platform</h5>
            <ul class="list-unstyled footer-links">
              <li><router-link to="/login">Admin Portal</router-link></li>
              <li><a href="#">About Us</a></li>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom mt-5 pt-4 d-flex justify-content-between align-items-center flex-wrap">
          <p class="mb-0 small" style="color: #a9a2b1;">Copyright © 2026 JobFinder. All rights reserved.</p>
          <p class="mb-0 small" style="color: #a9a2b1;">Browse by: <a href="#" class="text-decoration-none" style="color: #a9a2b1;">Jobs</a>, <a href="#" class="text-decoration-none" style="color: #a9a2b1;">Companies</a>, <a href="#" class="text-decoration-none" style="color: #a9a2b1;">Students</a></p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from './services/api'

const router = useRouter()
const route = useRoute()

const globalSearch = ref('')
const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

const isLoggedIn = computed(() => {
  // Access route.path to trigger reactivity on route change
  const path = route.path;
  return !!localStorage.getItem('token')
})

const userRole = computed(() => {
  const path = route.path;
  return localStorage.getItem('role') || 'student';
})

const fetchNotifications = async () => {
  if (!isLoggedIn.value) return;
  try {
    const res = await api.get('/notification/');
    notifications.value = res.data;
  } catch (err) {
    console.error('Failed to fetch notifications', err);
  }
}

const markAsRead = async (id) => {
  try {
    await api.put(`/notification/${id}/read`);
    fetchNotifications();
  } catch (err) {
    console.error('Failed to mark read', err);
  }
}

const handleSearch = () => {
  if (globalSearch.value.trim()) {
    const q = encodeURIComponent(globalSearch.value);
    if (userRole.value === 'student') {
      router.push(`/student/jobs?search=${q}`)
    } else if (userRole.value === 'company') {
      router.push(`/company/jobs?search=${q}`)
    } else if (userRole.value === 'admin') {
      router.push(`/admin/search?search=${q}`)
    }
  }
}

let notifInterval;
onMounted(() => {
  if (isLoggedIn.value) fetchNotifications();
  notifInterval = setInterval(() => {
    if (isLoggedIn.value) fetchNotifications();
  }, 15000); // Check every 15s
})

onUnmounted(() => {
  clearInterval(notifInterval);
})

// Refetch notifications on route change to keep them updated
watch(() => route.path, () => {
  if (isLoggedIn.value) fetchNotifications();
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  clearInterval(notifInterval)
  notifications.value = []
  router.push('/login')
}
</script>

<style>
body {
  background-color: #fbfbfe;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.tracking-tight {
  letter-spacing: -0.05em;
}

.navbar {
  z-index: 1000;
  position: relative;
}

/* Custom Nav Buttons Hover Effects */
.nav-btn-signup {
  background-color: #0b0f19; /* very dark blue/black */
  color: #ffffff !important;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-btn-signup:hover {
  background-color: #00008b; /* dark blue */
  box-shadow: 0 0 0 5px rgba(0, 0, 139, 0.25);
  transform: translateY(-1px);
}

.nav-btn-login {
  color: #0b0f19 !important;
  border: 1px solid transparent;
  border-radius: 50px;
  transition: all 0.2s ease;
}

.nav-btn-login:hover {
  border-color: #00008b;
  color: #00008b !important;
  background-color: rgba(0, 0, 139, 0.05);
  box-shadow: 0 0 0 5px rgba(0, 0, 139, 0.15);
  transform: translateY(-1px);
}

/* Footer Styles */
.app-footer {
  background-color: #181124; /* Very dark purple/black */
  color: #ffffff;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: #a9a2b1;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #ffffff;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Custom Navbar Icons */
.custom-nav-icon {
  transition: all 0.2s ease;
}
.custom-nav-icon:hover {
  color: #00008b !important;
  transform: translateY(-1px);
}

.profile-avatar {
  cursor: pointer;
  transition: all 0.2s ease;
}
.nav-link:hover .profile-avatar {
  border-color: #00008b !important;
  color: #00008b !important;
}

.hide-caret::after {
  display: none !important;
}

.dropdown-item {
  transition: all 0.2s ease;
}
.dropdown-item:hover {
  background-color: rgba(0, 0, 139, 0.05);
  color: #00008b;
}
.dropdown-item.text-danger:hover {
  background-color: rgba(220, 53, 69, 0.05);
  color: #dc3545 !important;
}

/* Scrollbar for Notifications */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1; 
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8; 
}
</style>
