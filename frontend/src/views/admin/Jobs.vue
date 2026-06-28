<template>
  <div class="mt-4">
    <h2>Manage Placement Drives</h2>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Company Name</th>
            <th>Job Title</th>
            <th>Created At</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.id }}</td>
            <td>{{ job.company_name }}</td>
            <td>{{ job.title }}</td>
            <td>{{ new Date(job.created_at).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="statusClass(job.status)">
                {{ job.status }}
              </span>
            </td>
            <td>
              <button v-if="job.status === 'Pending'" @click="approveJob(job.id)" class="btn btn-sm btn-success me-1">Approve</button>
              <button v-if="job.status === 'Pending'" @click="rejectJob(job.id)" class="btn btn-sm btn-danger">Reject</button>
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
      jobs: []
    }
  },
  mounted() {
    this.fetchJobs();
  },
  methods: {
    async fetchJobs() {
      try {
        const response = await api.get('/admin/jobs');
        this.jobs = response.data;
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    statusClass(status) {
      if (status === 'Approved') return 'bg-success';
      if (status === 'Pending') return 'bg-warning';
      if (status === 'Rejected') return 'bg-danger';
      return 'bg-secondary';
    },
    async approveJob(id) {
      if (confirm('Are you sure you want to approve this job?')) {
        try {
          await api.post(`/admin/jobs/${id}/approve`);
          this.fetchJobs();
        } catch (error) {
          console.error(error);
        }
      }
    },
    async rejectJob(id) {
      if (confirm('Are you sure you want to reject this job?')) {
        try {
          await api.post(`/admin/jobs/${id}/reject`);
          this.fetchJobs();
        } catch (error) {
          console.error(error);
        }
      }
    }
  }
}
</script>
