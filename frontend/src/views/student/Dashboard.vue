<template>
  <div class="mt-4">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4">
        <div class="list-group">
          <router-link to="/student" class="list-group-item list-group-item-action" exact-active-class="active">Overview</router-link>
          <router-link to="/student/profile" class="list-group-item list-group-item-action" active-class="active">My Profile</router-link>
          <router-link to="/student/jobs" class="list-group-item list-group-item-action" active-class="active">Browse Jobs</router-link>
          <router-link to="/student/applications" class="list-group-item list-group-item-action" active-class="active">My Applications</router-link>
          <router-link to="/student/exports" class="list-group-item list-group-item-action" active-class="active">Data Exports</router-link>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <router-view></router-view>
        
        <!-- Overview Stats -->
        <div v-if="$route.path === '/student'">
          <h2 class="mb-4">Student Overview</h2>
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="card bg-primary text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Jobs Applied</h5>
                  <h2 class="display-4">{{ stats.applications }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-info text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Shortlisted</h5>
                  <h2 class="display-4">{{ stats.shortlisted }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-success text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Offers Received</h5>
                  <h2 class="display-4">{{ stats.selected }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card bg-danger text-white h-100">
                <div class="card-body">
                  <h5 class="card-title">Rejected</h5>
                  <h2 class="display-4">{{ stats.rejected }}</h2>
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
        applications: 0,
        shortlisted: 0,
        selected: 0,
        rejected: 0
      }
    }
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await api.get('/student/stats');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    }
  }
}
</script>
