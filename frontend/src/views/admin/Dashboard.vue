<template>
  <div class="mt-4">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4">
        <div class="list-group">
          <router-link to="/admin" class="list-group-item list-group-item-action" exact-active-class="active">Overview</router-link>
          <router-link to="/admin/companies" class="list-group-item list-group-item-action" active-class="active">Companies</router-link>
          <router-link to="/admin/students" class="list-group-item list-group-item-action" active-class="active">Students</router-link>
          <router-link to="/admin/jobs" class="list-group-item list-group-item-action" active-class="active">Placement Drives</router-link>
          <router-link to="/admin/applications" class="list-group-item list-group-item-action" active-class="active">Applications</router-link>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <router-view></router-view>
        
        <!-- Overview Stats (Only show when at /admin exactly) -->
        <div v-if="$route.path === '/admin'">
          <h2 class="mb-4">Admin Overview</h2>
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="card bg-primary text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Total Students</h5>
                  <h2 class="display-4">{{ stats.students }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-success text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Total Companies</h5>
                  <h2 class="display-4">{{ stats.companies }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-info text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Placement Drives</h5>
                  <h2 class="display-4">{{ stats.jobs }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-warning text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Applications</h5>
                  <h2 class="display-4">{{ stats.applications }}</h2>
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
        students: 0,
        companies: 0,
        jobs: 0,
        applications: 0
      }
    }
  },
  mounted() {
    this.fetchStats();
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
