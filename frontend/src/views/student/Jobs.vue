<template>
  <div class="pb-5">
    <!-- Header -->
    <h3 class="fw-bold mb-4">Search for jobs</h3>
    
    <!-- Search Box -->
    <div class="mb-4 mt-3">
      <input type="text" v-model="search" @input="fetchJobs" class="form-control form-control-lg border-2 shadow-sm" placeholder="Search by job title, company, or skills...">
    </div>

    <!-- Job Cards List -->
    <div class="d-flex flex-column gap-3">
      <div v-for="job in jobs" :key="job.id" class="card border rounded-3 bg-white overflow-hidden shadow-sm">
        
        <!-- Company Header part -->
        <div class="p-4 border-bottom position-relative">
          <div class="d-flex align-items-start gap-3">
            <div class="border rounded-3 d-flex align-items-center justify-content-center bg-light overflow-hidden" style="width: 64px; height: 64px;">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
            </div>
            <div class="flex-grow-1">
              <h5 class="fw-bold mb-1 text-dark" style="font-size: 16px;">{{ job.company_name }}</h5>
              <div class="text-dark fw-medium mb-1" style="font-size: 14px;">{{ job.description || 'No description provided' }}</div>
            </div>
          </div>
        </div>

        <!-- Role inner block -->
        <div class="p-4 bg-white">
          <div class="border rounded-2 p-3 bg-white" style="border-color: #e5e7eb;">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center gap-3">
              <div>
                <h6 class="fw-bold mb-1 text-dark" style="font-size: 15px;">{{ job.title }}</h6>
                <div class="text-muted" style="font-size: 13px;">
                  Salary: {{ job.salary || 'Not specified' }} • Skills: {{ job.skills_required || 'Not specified' }}
                </div>
              </div>
              <div class="d-flex align-items-center gap-3 w-100 w-md-auto justify-content-end">
                <div class="text-end d-none d-md-block">
                  <div class="text-muted" style="font-size: 9px; font-weight: 600; letter-spacing: 0.5px;">{{ getDaysAgoText(job.created_at) }}</div>
                  <div class="mt-1" style="font-size: 9px; font-weight: 700; color: #dc2626; letter-spacing: 0.5px;" v-if="job.deadline">
                    DEADLINE: {{ new Date(job.deadline).toLocaleDateString() }}
                  </div>
                  <div class="mt-1 text-muted" style="font-size: 9px; font-weight: 700; letter-spacing: 0.5px;" v-else>
                    NO DEADLINE
                  </div>
                </div>
                <button v-if="!job.has_applied" class="btn btn-dark fw-bold btn-sm px-4 py-1" style="font-size: 14px;" @click="applyJob(job.id)">Apply</button>
                <button v-else class="btn btn-success fw-bold btn-sm px-4 py-1" style="font-size: 14px;" disabled>Applied</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="jobs.length === 0" class="col-12 text-center text-muted py-5 border rounded-3 bg-white shadow-sm">
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
    if (this.$route.query.search) {
      this.search = this.$route.query.search;
    }
    this.fetchJobs();
  },
  watch: {
    '$route.query.search': function(newVal) {
      this.search = newVal || '';
      this.fetchJobs();
    }
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
    },
    getDaysAgoText(dateString) {
      if (!dateString) return 'POSTED TODAY';
      const date = new Date(dateString);
      const today = new Date();
      const diffTime = today.getTime() - date.getTime();
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24)); 
      if (diffDays === 0) return 'POSTED TODAY';
      if (diffDays === 1) return 'POSTED 1 DAY AGO';
      return `POSTED ${diffDays} DAYS AGO`;
    }
  }
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}
.hover-shadow-sm:hover {
  box-shadow: 0 .125rem .25rem rgba(0,0,0,.075) !important;
}
.hover-text-dark:hover {
  color: #212529 !important;
}
.transition-all {
  transition: all 0.2s ease-in-out;
}
.form-check-input:checked {
  background-color: #2563eb;
  border-color: #2563eb;
}
</style>
