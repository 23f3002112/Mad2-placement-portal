<template>
  <div class="mt-4">
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4">
        <div class="list-group">
          <router-link to="/company" class="list-group-item list-group-item-action" exact-active-class="active">Overview</router-link>
          <router-link to="/company/profile" class="list-group-item list-group-item-action" active-class="active">Company Profile</router-link>
          <router-link to="/company/jobs" class="list-group-item list-group-item-action" active-class="active">Manage Jobs</router-link>
          <router-link to="/company/applications" class="list-group-item list-group-item-action" active-class="active">Manage Applications</router-link>
          <router-link to="/company/exports" class="list-group-item list-group-item-action" active-class="active">Data Exports</router-link>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <router-view></router-view>
        
        <!-- Overview Stats -->
        <div v-if="$route.path === '/company'">
          <h2 class="mb-4">Company Overview</h2>
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="card bg-primary text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Total Jobs Posted</h5>
                  <h2 class="display-4">{{ stats.total_jobs }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-success text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Active Approved Jobs</h5>
                  <h2 class="display-4">{{ stats.active_jobs }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-info text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Total Applications</h5>
                  <h2 class="display-4">{{ stats.applications }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-warning text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Shortlisted Candidates</h5>
                  <h2 class="display-4">{{ stats.shortlisted }}</h2>
                </div>
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
  methods: {
    async fetchStats() {
      try {
        const response = await api.get('/company/stats');
        this.stats = response.data;
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
