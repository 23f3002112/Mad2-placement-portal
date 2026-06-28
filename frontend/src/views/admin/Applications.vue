<template>
  <div class="mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>All Applications</h2>
    </div>

    <div class="table-responsive">
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Student</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Date Applied</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.id }}</td>
            <td>{{ app.student_name }}</td>
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ new Date(app.date_applied).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="statusClass(app.status)">{{ app.status }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-info" @click="viewProfile(app.student_id)">View Profile</button>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="7" class="text-center text-muted">No applications found in the system.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Student Profile Modal -->
    <div v-if="showProfileModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Student Profile & History</h5>
            <button type="button" class="btn-close" @click="closeProfileModal"></button>
          </div>
          <div class="modal-body" v-if="selectedStudent">
            <div class="row mb-4">
              <div class="col-md-6">
                <p><strong>Name:</strong> {{ selectedStudent.name }}</p>
                <p><strong>Email:</strong> {{ selectedStudent.email }}</p>
                <p><strong>Education:</strong> {{ selectedStudent.education }}</p>
              </div>
              <div class="col-md-6">
                <p><strong>Skills:</strong> {{ selectedStudent.skills }}</p>
                <p><strong>Resume URL:</strong> <a :href="selectedStudent.resume_url" target="_blank" v-if="selectedStudent.resume_url">View Resume</a><span v-else>None</span></p>
              </div>
              <div class="col-12 mt-2">
                <p><strong>Experience:</strong><br/> <span style="white-space: pre-wrap">{{ selectedStudent.experience || 'None provided' }}</span></p>
              </div>
            </div>
            
            <h6>Application History</h6>
            <div class="table-responsive">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="app in selectedStudent.applications" :key="app.id">
                    <td>{{ app.company_name }}</td>
                    <td>{{ app.job_title }}</td>
                    <td>{{ new Date(app.date_applied).toLocaleDateString() }}</td>
                    <td><span class="badge" :class="statusClass(app.status)">{{ app.status }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeProfileModal">Close</button>
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
      showProfileModal: false,
      selectedStudent: null
    }
  },
  mounted() {
    this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      try {
        const response = await api.get('/admin/applications');
        this.applications = response.data;
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    },
    async viewProfile(studentId) {
      try {
        const response = await api.get(`/admin/students/${studentId}`);
        this.selectedStudent = response.data;
        this.showProfileModal = true;
      } catch (error) {
        console.error('Error fetching student details:', error);
      }
    },
    closeProfileModal() {
      this.showProfileModal = false;
      this.selectedStudent = null;
    },
    statusClass(status) {
      if (status === 'Placed') return 'bg-success';
      if (status === 'Offer' || status === 'Selected') return 'bg-success bg-opacity-75';
      if (status === 'Interview') return 'bg-warning text-dark';
      if (status === 'Shortlisted') return 'bg-info text-dark';
      if (status === 'Rejected') return 'bg-danger';
      return 'bg-secondary';
    }
  }
}
</script>
