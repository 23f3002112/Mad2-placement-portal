<template>
  <div class="mt-4">
    <h2>Manage Applications</h2>
    <div v-if="!jobId" class="alert alert-info">
      Please select a job from the <router-link to="/company/jobs">Manage Jobs</router-link> page to view its applications.
    </div>
    
    <div v-else class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>App ID</th>
            <th>Student Name</th>
            <th>Education</th>
            <th>Skills</th>
            <th>Date Applied</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.id }}</td>
            <td>{{ app.student_name }}</td>
            <td>{{ app.education }}</td>
            <td>{{ app.skills }}</td>
            <td>{{ new Date(app.date_applied).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="statusClass(app.status)">{{ app.status }}</span>
              <div v-if="app.interview_date" class="small text-muted mt-1">
                Interview: {{ new Date(app.interview_date).toLocaleString() }}
              </div>
            </td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="openProfile(app)">View Profile</button>
              <button class="btn btn-sm btn-primary" @click="openModal(app)">Update Status</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Update Status Modal -->
    <div v-if="showModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update Application Status</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="updateStatus">
            <div class="modal-body">
              <div class="mb-3">
                <label>Status</label>
                <select v-model="updateForm.status" class="form-select">
                  <option value="Applied">Applied</option>
                  <option value="Shortlisted">Shortlisted</option>
                  <option value="Interview">Interview</option>
                  <option value="Offer">Offer</option>
                  <option value="Placed">Placed</option>
                  <option value="Rejected">Rejected</option>
                </select>
              </div>
              <div class="mb-3">
                <label>Feedback</label>
                <textarea v-model="updateForm.feedback" class="form-control" rows="3" placeholder="Provide feedback to the student"></textarea>
              </div>
              <div class="mb-3" v-if="updateForm.status === 'Shortlisted'">
                <label>Schedule Interview Date & Time</label>
                <input type="datetime-local" v-model="updateForm.interview_date" class="form-control">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Profile Modal -->
    <div v-if="showProfileModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Student Profile</h5>
            <button type="button" class="btn-close" @click="showProfileModal = false"></button>
          </div>
          <div class="modal-body" v-if="selectedProfile">
            <p><strong>Name:</strong> {{ selectedProfile.student_name }}</p>
            <p><strong>Email:</strong> {{ selectedProfile.email }}</p>
            <p><strong>Education:</strong> {{ selectedProfile.education }}</p>
            <p><strong>Skills:</strong> {{ selectedProfile.skills }}</p>
            <p><strong>Experience:</strong><br/> <span style="white-space: pre-wrap">{{ selectedProfile.experience || 'None provided' }}</span></p>
            <p><strong>Resume URL:</strong> <a :href="selectedProfile.resume_url" target="_blank" v-if="selectedProfile.resume_url">View Resume</a><span v-else>None</span></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showProfileModal = false">Close</button>
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
      jobId: null,
      showModal: false,
      showProfileModal: false,
      selectedProfile: null,
      updateForm: {
        id: null,
        status: '',
        feedback: '',
        interview_date: ''
      }
    }
  },
  mounted() {
    this.jobId = this.$route.query.job_id;
    if (this.jobId) {
      this.fetchApplications();
    }
  },
  watch: {
    '$route.query.job_id'(newId) {
      this.jobId = newId;
      if (this.jobId) {
        this.fetchApplications();
      }
    }
  },
  methods: {
    async fetchApplications() {
      try {
        const response = await api.get(`/company/jobs/${this.jobId}/applications`);
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
    openProfile(app) {
      this.selectedProfile = app;
      this.showProfileModal = true;
    },
    openModal(app) {
      this.updateForm = {
        id: app.id,
        status: app.status,
        feedback: app.feedback || '',
        interview_date: app.interview_date ? app.interview_date.substring(0, 16) : '' // format for datetime-local
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.updateForm = { id: null, status: '', feedback: '', interview_date: '' };
    },
    async updateStatus() {
      try {
        let payload = {
          status: this.updateForm.status,
          feedback: this.updateForm.feedback
        };
        if ((this.updateForm.status === 'Shortlisted' || this.updateForm.status === 'Interview') && this.updateForm.interview_date) {
          payload.interview_date = new Date(this.updateForm.interview_date).toISOString();
        }
        
        await api.put(`/company/applications/${this.updateForm.id}/status`, payload);
        this.closeModal();
        this.fetchApplications();
      } catch (error) {
        console.error('Error updating application:', error);
      }
    }
  }
}
</script>
