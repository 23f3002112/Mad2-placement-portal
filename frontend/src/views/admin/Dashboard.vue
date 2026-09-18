<script setup>
import { Briefcase, Building, FileText, Home, Users } from 'lucide-vue-next';
</script>

<template>
  <div class="mt-4">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4 position-sticky" style="top: 20px; height: calc(100vh - 40px);">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body p-0 py-3 d-flex flex-column">
            <div class="list-group list-group-flush border-0">
              <router-link to="/admin" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" exact-active-class="active">
                <Home class="me-3" :size="20" /> Overview
              </router-link>
              <router-link to="/admin/companies" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <Building class="me-3" :size="20" /> Companies
              </router-link>
              <router-link to="/admin/students" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <Users class="me-3" :size="20" /> Students
              </router-link>
              <router-link to="/admin/jobs" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <Briefcase class="me-3" :size="20" /> Placement Drives
              </router-link>
              <router-link to="/admin/applications" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active">
                <FileText class="me-3" :size="20" /> Applications
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
                    <Users />
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
                    <Building />
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
                    <Briefcase />
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
                    <FileText />
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
