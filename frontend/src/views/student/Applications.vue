<template>
  <div class="pb-5">
    <h3 class="fw-bold mb-4">My Applications</h3>
    
    <div class="table-responsive bg-white rounded shadow-sm">
      <table class="table table-hover align-middle mb-0" style="border: 1px solid #f1f3f5;">
        <thead class="bg-white">
          <tr style="border-bottom: 2px solid #f1f3f5;">
            <th class="py-3 text-dark fw-bold border-0 px-4" style="font-size: 14px;">Company</th>
            <th class="py-3 text-dark fw-bold border-0" style="font-size: 14px;">Job Title</th>
            <th class="py-3 text-dark fw-bold border-0" style="font-size: 14px;">Date Applied</th>
            <th class="py-3 text-dark fw-bold border-0" style="font-size: 14px;">Status</th>
            <th class="py-3 text-dark fw-bold border-0 px-4" style="font-size: 14px;">Details</th>
          </tr>
        </thead>
        <tbody class="border-top-0">
          <tr v-for="app in applications" :key="app.id" style="border-bottom: 1px solid #f1f3f5;">
            <td class="py-3 text-dark px-4 border-0" style="font-size: 14px;">{{ app.company_name }}</td>
            <td class="py-3 text-dark border-0" style="font-size: 14px;">{{ app.job_title }}</td>
            <td class="py-3 text-dark border-0" style="font-size: 14px;">{{ new Date(app.date_applied).toLocaleDateString() }}</td>
            <td class="py-3 border-0">
              <span class="badge rounded-pill px-3 py-2" :class="statusClass(app.status)" style="font-size: 11px; font-weight: 600; letter-spacing: 0.3px;">{{ app.status }}</span>
            </td>
            <td class="py-3 px-4 border-0">
              <button class="btn btn-sm btn-outline-primary px-3 fw-medium" style="font-size: 12px; border-radius: 4px;" @click="viewDetails(app)">View</button>
              <template v-if="app.status === 'Offer'">
                <button class="btn btn-sm btn-success ms-2 px-3 fw-medium" style="font-size: 12px; border-radius: 4px;" @click="respondOffer(app, 'Placed')">Accept</button>
                <button class="btn btn-sm btn-danger ms-2 px-3 fw-medium" style="font-size: 12px; border-radius: 4px;" @click="respondOffer(app, 'Rejected')">Reject</button>
              </template>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center text-muted py-5 border-0">You have not applied to any jobs yet.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Application Details Modal -->
    <div v-if="selectedApp" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.4); backdrop-filter: blur(2px);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-3">
          <div class="modal-header border-bottom-0 pb-0 pt-4 px-4">
            <h5 class="modal-title fw-normal text-dark" style="font-size: 20px;">Application Details</h5>
            <button type="button" class="btn-close shadow-none" @click="selectedApp = null" style="font-size: 14px; opacity: 0.6;"></button>
          </div>
          <div class="modal-body px-4 pt-4 pb-3">
            <div class="d-flex flex-column gap-3 text-dark" style="font-size: 15px;">
              <div><span class="fw-bold me-1">Company:</span> {{ selectedApp.company_name }}</div>
              <div><span class="fw-bold me-1">Job Title:</span> {{ selectedApp.job_title }}</div>
              <div><span class="fw-bold me-1">Salary:</span> {{ selectedApp.salary || 'Not specified' }}</div>
              <div><span class="fw-bold me-1">Skills:</span> {{ selectedApp.skills_required || 'Not specified' }}</div>
              <div><span class="fw-bold me-1">Description:</span> <span style="font-size: 14px;">{{ selectedApp.description || 'No description provided' }}</span></div>
              <div class="mt-2">
                <span class="fw-bold me-2 align-middle">Status:</span> 
                <span class="badge rounded-pill px-3 py-1 align-middle" :class="statusClass(selectedApp.status)" style="font-size: 12px; font-weight: 600; letter-spacing: 0.3px;">{{ selectedApp.status }}</span>
              </div>
            </div>
            
            <hr class="text-muted opacity-25 my-4">
            
            <div v-if="selectedApp.interview_date">
              <h6 class="fw-bold text-dark mb-2" style="font-size: 15px;">Interview Scheduled:</h6>
              <div class="text-dark">{{ new Date(selectedApp.interview_date).toLocaleString() }}</div>
            </div>
            
            <div v-if="selectedApp.feedback" class="mt-3">
              <h6 class="fw-bold text-dark mb-2" style="font-size: 15px;">Company Feedback:</h6>
              <div class="p-3 bg-light rounded text-dark" style="font-size: 14px; border: 1px solid #f1f3f5;">{{ selectedApp.feedback }}</div>
            </div>
            
            <div v-if="!selectedApp.interview_date && !selectedApp.feedback" class="text-muted" style="font-size: 15px;">
              No additional feedback or interview scheduled yet.
            </div>
          </div>
          <div class="modal-footer border-top-0 px-4 pb-4 pt-2">
            <button v-if="selectedApp.status === 'Selected'" class="btn btn-success me-auto px-4 fw-medium" @click="downloadOffer(selectedApp)">Download Offer Letter</button>
            <button type="button" class="btn text-white px-4 fw-medium shadow-sm" style="background-color: #64748b; border: none; border-radius: 6px;" @click="selectedApp = null">Close</button>
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
      if (status === 'Placed') return 'bg-success';
      if (status === 'Offer' || status === 'Selected') return 'bg-success bg-opacity-75';
      if (status === 'Interview') return 'bg-warning text-dark';
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
    },
    async respondOffer(app, status) {
      if (!confirm(`Are you sure you want to ${status === 'Placed' ? 'accept' : 'reject'} this offer?`)) return;
      try {
        await api.put(`/student/applications/${app.id}/respond`, { status });
        this.fetchApplications();
        alert(`You have ${status === 'Placed' ? 'accepted' : 'rejected'} the offer.`);
      } catch (error) {
        console.error('Error responding to offer:', error);
        alert('An error occurred. Please try again.');
      }
    }
  }
}
</script>
