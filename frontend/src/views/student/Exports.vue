<template>
  <div class="mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Data Exports</h2>
      <button class="btn btn-primary" @click="triggerExport" :disabled="isExporting">
        <span v-if="isExporting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        {{ isExporting ? 'Starting Export...' : 'Export Application History (CSV)' }}
      </button>
    </div>

    <div v-if="message" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="card-title mb-3">Export Jobs</h5>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Job ID</th>
                <th>Requested At</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="job in jobs" :key="job.id">
                <td>{{ job.id }}</td>
                <td>{{ new Date(job.created_at).toLocaleString() }}</td>
                <td>
                  <span class="badge" :class="{
                    'bg-warning text-dark': job.status === 'Pending',
                    'bg-success': job.status === 'Completed',
                    'bg-danger': job.status === 'Failed'
                  }">{{ job.status }}</span>
                </td>
                <td>
                  <button v-if="job.status === 'Completed'" 
                     @click="downloadFile(job.id)" 
                     class="btn btn-sm btn-outline-success">
                    Download CSV
                  </button>
                  <span v-else-if="job.status === 'Pending'" class="text-muted small">
                    Processing...
                  </span>
                </td>
              </tr>
              <tr v-if="jobs.length === 0">
                <td colspan="4" class="text-center text-muted">No exports requested yet.</td>
              </tr>
            </tbody>
          </table>
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
      jobs: [],
      isExporting: false,
      message: '',
      pollInterval: null
    }
  },
  mounted() {
    this.fetchExports();
    // Poll every 5 seconds to update statuses
    this.pollInterval = setInterval(this.fetchExports, 5000);
  },
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  },
  methods: {
    async fetchExports() {
      try {
        const response = await api.get('/student/exports');
        this.jobs = response.data;
      } catch (error) {
        console.error('Error fetching exports:', error);
      }
    },
    async triggerExport() {
      this.isExporting = true;
      try {
        const response = await api.post('/student/export');
        this.message = "Export task started in the background. It will appear below shortly.";
        this.fetchExports();
      } catch (error) {
        console.error('Error starting export:', error);
      } finally {
        this.isExporting = false;
      }
    },
    async downloadFile(jobId) {
      try {
        const response = await api.get(`/student/exports/${jobId}/download`, {
          responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `export_${jobId}.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('Download failed:', error);
        alert('Failed to download file.');
      }
    }
  }
}
</script>
