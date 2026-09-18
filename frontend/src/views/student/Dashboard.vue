<script setup>
import { Briefcase, CheckCircle, FileText, Home, Mail, MessageSquare, Star, User } from 'lucide-vue-next';
</script>

<template>
  <div class="mt-4">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4 position-sticky" style="top: 20px; height: calc(100vh - 40px);">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body p-0 py-3 d-flex flex-column">
            <div class="list-group list-group-flush border-0">
              <router-link to="/student" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" exact-active-class="active"><Home class="me-3" :size="20" /> Home</router-link>
              <router-link to="/student/profile" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active"><User class="me-3" :size="20" /> Profile</router-link>
              <router-link to="/student/jobs" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active"><Briefcase class="me-3" :size="20" /> Jobs</router-link>
              <router-link to="/student/applications" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active"><FileText class="me-3" :size="20" /> Applied</router-link>
              <router-link to="/student/messages" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active"><MessageSquare class="me-3" :size="20" /> Messages</router-link>
            </div>
            
            <div class="list-group list-group-flush border-0 mt-auto">
              <router-link to="/student/exports" class="list-group-item list-group-item-action border-0 px-4 py-3 fw-medium d-flex align-items-center" active-class="active"><Mail class="me-3" :size="20" /> Data Exports</router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <!-- Profile Incomplete Alert -->
        <div v-if="isProfileIncomplete" class="card border mb-4 shadow-sm rounded-3 overflow-hidden">
          <div class="card-body p-3 d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-3">
              <User />
              <span class="fw-medium text-dark" style="font-size: 15px;">Your profile can't be found by recruiters because it's missing key information</span>
            </div>
            <router-link to="/student/profile" class="text-decoration-none fw-medium d-flex align-items-center gap-1" style="color: #2563eb; font-size: 14px;">
              Complete your profile
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </router-link>
          </div>
        </div>

        <router-view></router-view>
        
        <!-- Overview Stats -->
        <div v-if="$route.path === '/student'">
          <h3 class="mb-4 fw-bold">Student Overview</h3>
          <div class="row mb-5">
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 110, 253, 0.1);">
                    <FileText />
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.applications }}</h2>
                <span class="text-muted fw-medium">Jobs Applied</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(13, 202, 240, 0.1);">
                    <Star />
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.shortlisted }}</h2>
                <span class="text-muted fw-medium">Shortlisted</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(25, 135, 84, 0.1);">
                    <CheckCircle />
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.selected }}</h2>
                <span class="text-muted fw-medium">Offers Received</span>
              </div>
            </div>
            
            <div class="col-md-3 col-6 mb-3">
              <div class="card border-0 shadow-sm rounded-4 h-100 p-3 bg-white">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; background-color: rgba(220, 53, 69, 0.1);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
                  </div>
                </div>
                <h2 class="display-6 fw-bold mb-1">{{ stats.rejected }}</h2>
                <span class="text-muted fw-medium">Rejected</span>
              </div>
            </div>
          </div>
          
          <!-- Recommended Jobs Section -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h4 class="fw-bold mb-0">Recommended Jobs</h4>
              <p class="text-muted small mb-0 mt-1">Jobs where you're a top applicant based on your profile.</p>
            </div>
            <router-link to="/student/jobs" class="text-decoration-none fw-medium text-primary">View all jobs</router-link>
          </div>
          
          <div class="row">
            <div class="col-12 mb-3" v-for="job in recommendedJobs" :key="job.id">
              <div class="card border-0 shadow-sm rounded-4 p-4">
                <div class="d-flex justify-content-between align-items-start">
                  <div class="d-flex gap-3">
                    <div class="rounded-3 bg-light d-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                      <Briefcase />
                    </div>
                    <div>
                      <h5 class="fw-bold mb-1">{{ job.title }}</h5>
                      <p class="text-muted mb-2">{{ job.company_name }}</p>
                      <div class="d-flex align-items-center gap-3 text-secondary small fw-medium">
                        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-1"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg> {{ job.salary || 'Not specified' }}</span>
                        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-1"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg> {{ job.skills_required || 'Any' }}</span>
                      </div>
                      <div class="mt-3 text-muted small">Posted {{ new Date(job.created_at).toLocaleDateString() }}</div>
                    </div>
                  </div>
                  <div>
                    <button class="btn btn-outline-dark rounded-pill px-4 fw-medium" v-if="!job.has_applied" @click="applyJob(job.id)">Apply</button>
                    <button class="btn btn-light rounded-pill px-4 fw-medium text-success" v-else disabled>Applied</button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="recommendedJobs.length === 0" class="col-12 text-center text-muted py-5 bg-white rounded-4 shadow-sm">
              <p class="mb-0">No recommended jobs found at the moment.</p>
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
      },
      recommendedJobs: [],
      profile: null
    }
  },
  computed: {
    isProfileIncomplete() {
      if (!this.profile) return false;
      const p = this.profile;
      return !p.education || !p.skills || !p.resume_url;
    }
  },
  mounted() {
    this.fetchProfile();
    if (this.$route.path === '/student') {
      this.fetchStats();
      this.fetchRecommendedJobs();
    }
  },
  watch: {
    '$route.path': function(newPath) {
      if (newPath === '/student') {
        this.fetchStats();
        this.fetchRecommendedJobs();
      }
      this.fetchProfile(); // Re-fetch on navigation to update banner status
    }
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await api.get('/student/profile');
        this.profile = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async fetchStats() {
      try {
        const response = await api.get('/student/stats');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    },
    async fetchRecommendedJobs() {
      try {
        const response = await api.get('/student/jobs');
        // Filter out jobs already applied to and slice top 3
        this.recommendedJobs = response.data.filter(j => !j.has_applied).slice(0, 3);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    async applyJob(jobId) {
      if (confirm('Are you sure you want to apply for this job?')) {
        try {
          await api.post('/student/applications', { job_id: jobId });
          alert('Application submitted successfully!');
          this.fetchStats();
          this.fetchRecommendedJobs();
        } catch (error) {
          const msg = error.response?.data?.msg || 'Error submitting application';
          alert(msg);
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
