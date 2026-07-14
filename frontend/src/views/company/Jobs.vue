<template>
  <div class="mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Manage Job Postings</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">Post New Job</button>
    </div>

    <!-- Create Job Modal -->
    <div v-if="showCreateModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Post a New Job</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <form @submit.prevent="createJob">
            <div class="modal-body">
              <div class="mb-3">
                <label>Job Title</label>
                <input type="text" v-model="newJob.title" class="form-control" required>
              </div>
              <div class="mb-3">
                <label>Description</label>
                <textarea v-model="newJob.description" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label>Salary</label>
                <input type="text" v-model="newJob.salary" class="form-control" placeholder="e.g. 50,000 USD">
              </div>
              <div class="mb-3">
                <label>Skills Required</label>
                <input type="text" v-model="newJob.skills_required" class="form-control" placeholder="e.g. Python, Vue, SQL">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showCreateModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary">Post Job</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Salary</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.id }}</td>
            <td>{{ job.title }}</td>
            <td>{{ job.salary }}</td>
            <td>
              <span class="badge" :class="statusClass(job.status)">{{ job.status }}</span>
            </td>
            <td>{{ new Date(job.created_at).toLocaleDateString() }}</td>
            <td>
              <button 
                v-if="job.status === 'Approved'" 
                @click="updateStatus(job.id, 'Closed')" 
                class="btn btn-sm btn-danger me-1">Close Job</button>
              <button 
                v-if="job.status === 'Closed'" 
                @click="updateStatus(job.id, 'Approved')" 
                class="btn btn-sm btn-success me-1">Re-open</button>
              <router-link :to="`/company/applications?job_id=${job.id}`" class="btn btn-sm btn-info">View Apps</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      jobs: [],
      search: '',
      showCreateModal: false,
      newJob: {
        title: '',
        description: '',
        salary: '',
        skills_required: ''
      }
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
        const response = await api.get(`/company/jobs?search=${this.search}`);
        this.jobs = response.data;
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    async createJob() {
      try {
        await api.post('/company/jobs', this.newJob);
        this.showCreateModal = false;
        this.newJob = { title: '', description: '', salary: '', skills_required: '' };
        this.fetchJobs();
        alert('Job created successfully. It will be visible to students once approved by the admin.');
      } catch (error) {
        console.error('Error creating job:', error);
      }
    },
    async updateStatus(id, status) {
      try {
        await api.put(`/company/jobs/${id}/status`, { status });
        this.fetchJobs();
      } catch (error) {
        console.error('Error updating status:', error);
      }
    },
    statusClass(status) {
      if (status === 'Approved') return 'bg-success';
      if (status === 'Pending') return 'bg-warning text-dark';
      if (status === 'Closed') return 'bg-secondary';
      if (status === 'Rejected') return 'bg-danger';
      return 'bg-primary';
    }
  }
}
</script>
