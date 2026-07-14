<template>
  <div class="mt-4">
    <div v-if="error" class="alert alert-danger shadow-sm border-0 rounded-4 p-5 text-center mt-5 mx-auto" style="max-width: 600px;">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-danger mb-3"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
      <h4 class="fw-bold text-dark">Account Pending Approval</h4>
      <p class="text-muted mb-0">{{ error }}</p>
    </div>
    
    <div v-else class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4 position-sticky" style="top: 20px; height: calc(100vh - 40px);">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body p-0 py-3 d-flex flex-column">
            <div class="list-group list-group-flush border-0">
              <router-link to="/company" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" exact-active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg> Overview
              </router-link>
              <router-link to="/company/profile" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg> Company Profile
              </router-link>
              <router-link to="/company/jobs" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg> Manage Jobs
              </router-link>
              <router-link to="/company/applications" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Applications
              </router-link>
              <router-link to="/company/messages" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg> Messages
              </router-link>
            </div>
            
            <div class="list-group list-group-flush border-0 mt-auto">
              <router-link to="/company/exports" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-3"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg> Data Exports
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <router-view></router-view>
        
        <!-- Overview Stats -->
        <div v-if="$route.path === '/company'">
          <h3 class="fw-bold mb-4">Company Overview</h3>
          <div class="row mb-5">
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 110, 253, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0d6efd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.total_jobs }}</h2>
                <span class="text-muted fw-medium">Total Jobs Posted</span>
              </div>
            </div>

            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(25, 135, 84, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#198754" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.active_jobs }}</h2>
                <span class="text-muted fw-medium">Active Jobs</span>
              </div>
            </div>

            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 202, 240, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0dcaf0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.applications }}</h2>
                <span class="text-muted fw-medium">Applications</span>
              </div>
            </div>

            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(255, 193, 7, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.shortlisted }}</h2>
                <span class="text-muted fw-medium">Shortlisted</span>
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
        total_jobs: 0,
        active_jobs: 0,
        applications: 0,
        shortlisted: 0
      },
      error: null
    }
  },
  mounted() {
    this.fetchStats();
  },
  watch: {
    '$route'(to, from) {
      if (to.path === '/company') {
        this.fetchStats();
      }
    }
  },
  methods: {
    async fetchStats() {
      try {
        const response = await api.get('/company/stats');
        this.stats = response.data;
        this.error = null;
      } catch (error) {
        if (error.response && error.response.status === 403) {
          this.error = error.response.data.msg || "Your company profile is pending admin approval. You cannot access dashboard features yet.";
        } else {
          console.error('Error fetching stats:', error);
        }
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
