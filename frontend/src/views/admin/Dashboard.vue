<template>
  <div class="mt-4">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4 position-sticky" style="top: 20px; height: calc(100vh - 40px);">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body p-0 py-3 d-flex flex-column">
            <div class="list-group list-group-flush border-0">
              <router-link to="/admin" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" exact-active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-3"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg> Overview
              </router-link>
              <router-link to="/admin/companies" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-3"><path d="M3 21h18"></path><path d="M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"></path><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"></path></svg> Companies
              </router-link>
              <router-link to="/admin/students" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-3"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg> Students
              </router-link>
              <router-link to="/admin/jobs" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-3"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg> Placement Drives
              </router-link>
              <router-link to="/admin/applications" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-3"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Applications
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <router-view></router-view>
        
        <!-- Overview Stats -->
        <div v-if="$route.path === '/admin'">
          <h3 class="mb-4 fw-bold">Admin Overview</h3>
          <div class="row mb-5">
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 110, 253, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0d6efd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.students }}</h2>
                <span class="text-muted fw-medium">Total Students</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(25, 135, 84, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#198754" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"></path><path d="M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"></path><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"></path></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.companies }}</h2>
                <span class="text-muted fw-medium">Total Companies</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 202, 240, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0dcaf0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.jobs }}</h2>
                <span class="text-muted fw-medium">Placement Drives</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(220, 53, 69, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.applications }}</h2>
                <span class="text-muted fw-medium">Applications</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      stats: {
        students: 0,
        companies: 0,
        jobs: 0,
        applications: 0
      }
    }
  },
  mounted() {
    if (this.$route.path === '/admin') {
      this.fetchStats();
    }
  },
  watch: {
    '$route.path': function(newPath) {
      if (newPath === '/admin') {
        this.fetchStats();
      }
    }
  },
  methods: {
    async fetchStats() {
      try {
        const response = await api.get('/admin/stats');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching admin stats:', error);
      }
    }
  }
}
</script>

<style scoped>
/* Sidebar link active styling */
.list-group-item.active {
  background-color: rgba(0, 0, 139, 0.05) !important;
  color: #00008b !important;
  border-right: 4px solid #00008b !important;
}
.list-group-item:hover {
  background-color: rgba(0, 0, 139, 0.02);
  color: #00008b !important;
}
</style>
