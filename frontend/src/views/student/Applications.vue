<template>
  <div class="mt-4">
    <h2>My Applications</h2>
    
    <div class="table-responsive mt-3">
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Date Applied</th>
            <th>Status</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ new Date(app.date_applied).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="statusClass(app.status)">{{ app.status }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-outline-primary" @click="viewDetails(app)">View</button>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center text-muted">You have not applied to any jobs yet.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Application Details Modal -->
    <div v-if="selectedApp" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Application Details</h5>
            <button type="button" class="btn-close" @click="selectedApp = null"></button>
          </div>
          <div class="modal-body">
            <p><strong>Company:</strong> {{ selectedApp.company_name }}</p>
            <p><strong>Job Title:</strong> {{ selectedApp.job_title }}</p>
            <p><strong>Status:</strong> <span class="badge" :class="statusClass(selectedApp.status)">{{ selectedApp.status }}</span></p>
            <hr>
            <div v-if="selectedApp.interview_date">
              <h6 class="text-primary">Interview Scheduled</h6>
              <p>{{ new Date(selectedApp.interview_date).toLocaleString() }}</p>
            </div>
            <div v-if="selectedApp.feedback">
              <h6>Company Feedback:</h6>
              <div class="p-3 bg-light rounded border">{{ selectedApp.feedback }}</div>
            </div>
            <div v-if="!selectedApp.interview_date && !selectedApp.feedback" class="text-muted">
              No additional feedback or interview scheduled yet.
            </div>
          </div>
          <div class="modal-footer">
            <button v-if="selectedApp.status === 'Selected'" class="btn btn-success me-auto" @click="downloadOffer(selectedApp)">Download Offer Letter</button>
            <button type="button" class="btn btn-secondary" @click="selectedApp = null">Close</button>
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
      applications: [],
      selectedApp: null
    }
  },
  mounted() {
    this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      try {
        const response = await api.get('/student/applications');
        this.applications = response.data;
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    },
    statusClass(status) {
      if (status === 'Selected') return 'bg-success';
      if (status === 'Shortlisted') return 'bg-info text-dark';
      if (status === 'Rejected') return 'bg-danger';
      return 'bg-secondary';
    },
    viewDetails(app) {
      this.selectedApp = app;
    },
    downloadOffer(app) {
      // Dummy action for downloading offer letter
      alert(`Downloading offer letter for ${app.job_title} at ${app.company_name}...`);
    }
  }
}
</script>
