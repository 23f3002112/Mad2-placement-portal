import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import CompanyDashboard from '../views/company/Dashboard.vue'
import StudentDashboard from '../views/student/Dashboard.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { 
    path: '/admin', 
    name: 'AdminDashboard', 
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: 'companies', name: 'AdminCompanies', component: () => import('../views/admin/Companies.vue') },
      { path: 'students', name: 'AdminStudents', component: () => import('../views/admin/Students.vue') },
      { path: 'jobs', name: 'AdminJobs', component: () => import('../views/admin/Jobs.vue') },
      { path: 'applications', name: 'AdminApplications', component: () => import('../views/admin/Applications.vue') }
    ]
  },
  { 
    path: '/company', 
    name: 'CompanyDashboard', 
    component: CompanyDashboard,
    meta: { requiresAuth: true, role: 'company' },
    children: [
      { path: 'profile', name: 'CompanyProfile', component: () => import('../views/company/Profile.vue') },
      { path: 'jobs', name: 'CompanyJobs', component: () => import('../views/company/Jobs.vue') },
      { path: 'applications', name: 'CompanyApplications', component: () => import('../views/company/Applications.vue') },
      { path: 'exports', name: 'CompanyExports', component: () => import('../views/company/Exports.vue') }
    ]
  },
  { 
    path: '/student', 
    name: 'StudentDashboard', 
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' },
    children: [
      { path: 'profile', name: 'StudentProfile', component: () => import('../views/student/Profile.vue') },
      { path: 'jobs', name: 'StudentJobs', component: () => import('../views/student/Jobs.vue') },
      { path: 'applications', name: 'StudentApplications', component: () => import('../views/student/Applications.vue') },
      { path: 'exports', name: 'StudentExports', component: () => import('../views/student/Exports.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAuth && to.meta.role !== userRole) {
    // Redirect to their respective dashboard if they try to access another role's route
    if (token && userRole) {
      next(`/${userRole}`)
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
