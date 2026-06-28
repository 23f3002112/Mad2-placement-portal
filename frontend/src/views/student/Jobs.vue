<template>
  <div class="mt-4">
    <h2>Browse Job Postings</h2>
    <div class="mb-4 mt-3">
      <input type="text" v-model="search" @input="fetchJobs" class="form-control" placeholder="Search by job title, company, or skills...">
    </div>
    
    <div class="row">
      <div class="col-md-6 mb-4" v-for="job in jobs" :key="job.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ job.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ job.company_name }}</h6>
            <p class="card-text">{{ job.description }}</p>
            <ul class="list-unstyled">
              <li><strong>Salary:</strong> {{ job.salary || 'Not specified' }}</li>
              <li><strong>Skills Required:</strong> {{ job.skills_required || 'Not specified' }}</li>
              <li><strong>Posted on:</strong> {{ new Date(job.created_at).toLocaleDateString() }}</li>
            </ul>
          </div>
          <div class="card-footer bg-white border-top-0">
            <button 
              v-if="!job.has_applied" 
              class="btn btn-primary w-100" 
              @click="applyJob(job.id)">
              Apply Now
            </button>
            <button 
              v-else 
              class="btn btn-success w-100" 
              disabled>
              Applied
            </button>
          </div>
        </div>
      </div>
      <div v-if="jobs.length === 0" class="col-12 text-center text-muted py-5">
        No active job postings found.
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      jobs: [],
      search: ''
    }
  },
  mounted() {
    this.fetchJobs();
  },
  methods: {
    async fetchJobs() {
      try {
        const response = await api.get(`/student/jobs?search=${this.search}`);
        this.jobs = response.data;
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    async applyJob(jobId) {
      if (confirm('Are you sure you want to apply for this job?')) {
        try {
          await api.post('/student/applications', { job_id: jobId });
          alert('Application submitted successfully!');
          this.fetchJobs();
        } catch (error) {
          const msg = error.response?.data?.msg || 'Error submitting application';
          alert(msg);
        }
      }
    }
  }
}
</script>
