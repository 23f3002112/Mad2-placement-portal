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
              <div v-if="app.interview_date && (app.status === 'Interview' || app.status === 'Shortlisted')" class="small text-muted mt-1">
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
              <template v-if="updateForm.status === 'Interview' || updateForm.status === 'Shortlisted'">
                <div class="mb-3">
                  <label>Schedule Interview Date & Time</label>
                  <input type="datetime-local" v-model="updateForm.interview_date" class="form-control" required>
                </div>
                <div class="mb-3" v-if="updateForm.status === 'Interview'">
                  <label class="d-block mb-2">Interview Type</label>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" v-model="updateForm.interview_type" value="Online" id="typeOnline">
                    <label class="form-check-label" for="typeOnline">Online</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" v-model="updateForm.interview_type" value="In-Person" id="typeInPerson">
                    <label class="form-check-label" for="typeInPerson">In-Person</label>
                  </div>
                </div>
                <div class="mb-3" v-if="updateForm.status === 'Interview' && updateForm.interview_type === 'Online'">
                  <label>Google Meet Link</label>
                  <input type="url" v-model="updateForm.interview_location_or_link" class="form-control" placeholder="https://meet.google.com/..." required>
                </div>
                <div class="mb-3" v-if="updateForm.status === 'Interview' && updateForm.interview_type === 'In-Person'">
                  <label>Location / Address</label>
                  <input type="text" v-model="updateForm.interview_location_or_link" class="form-control" placeholder="Office Address, Room No, etc." required>
                </div>
              </template>
              <template v-if="updateForm.status === 'Offer'">
                <div class="mb-3">
                  <label>Expected Joining Date</label>
                  <input type="date" v-model="updateForm.joining_date" class="form-control" required>
                </div>
                <div class="alert alert-info small mt-2 mb-0">
                  An official offer letter email will be sent to the candidate containing the job title and joining date.
                </div>
              </template>
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
        interview_date: '',
        interview_type: 'Online',
        interview_location_or_link: '',
        joining_date: ''
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
        interview_date: app.interview_date ? app.interview_date.substring(0, 16) : '',
        interview_type: app.interview_type || 'Online',
        interview_location_or_link: app.interview_location_or_link || '',
        joining_date: ''
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.updateForm = { id: null, status: '', feedback: '', interview_date: '', interview_type: 'Online', interview_location_or_link: '', joining_date: '' };
    },
    async updateStatus() {
      try {
        let payload = {
          status: this.updateForm.status,
          feedback: this.updateForm.feedback
        };
        if (this.updateForm.status === 'Shortlisted' || this.updateForm.status === 'Interview') {
          if (this.updateForm.interview_date) {
            payload.interview_date = new Date(this.updateForm.interview_date).toISOString();
          }
          if (this.updateForm.status === 'Interview') {
            payload.interview_type = this.updateForm.interview_type;
            payload.interview_location_or_link = this.updateForm.interview_location_or_link;
          }
        }
        if (this.updateForm.status === 'Offer') {
          payload.joining_date = this.updateForm.joining_date;
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
