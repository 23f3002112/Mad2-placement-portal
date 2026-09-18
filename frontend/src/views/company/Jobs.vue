<script setup>
import { Briefcase, CheckCircle, Edit, Eye, Trash2, Users, X } from 'lucide-vue-next';
</script>

<template>
  <div class="mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold mb-0">Manage Job Postings</h2>
      <button class="btn btn-primary px-4 fw-medium shadow-sm rounded-pill d-flex align-items-center" @click="openCreateModal">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        Post New Job
      </button>
    </div>

    <!-- Create/Edit Job Modal -->
    <div v-if="showModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow rounded-4">
          <div class="modal-header border-0 pb-0 pt-4 px-4">
            <h5 class="modal-title fw-bold">{{ isEditing ? 'Edit Job Posting' : 'Post a New Job' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveJob">
            <div class="modal-body p-4">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-medium">Job Title *</label>
                  <input type="text" v-model="jobForm.title" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-medium">Salary</label>
                  <input type="text" v-model="jobForm.salary" class="form-control" placeholder="e.g. 50,000 USD">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-medium">Skills Required</label>
                  <input type="text" v-model="jobForm.skills_required" class="form-control" placeholder="e.g. Python, Vue, SQL">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-medium">Application Deadline</label>
                  <input type="datetime-local" v-model="jobForm.deadline" class="form-control">
                </div>
                <div class="col-12 mb-3">
                  <label class="form-label fw-medium">Description *</label>
                  <textarea v-model="jobForm.description" class="form-control" rows="5" required></textarea>
                </div>
              </div>
            </div>
            <div class="modal-footer border-0 pt-0 pb-4 px-4">
              <button type="button" class="btn btn-light fw-medium rounded-pill px-4" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary fw-medium rounded-pill px-4">{{ isEditing ? 'Save Changes' : 'Post Job' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Details Modal -->
    <div v-if="showDetailsModal && selectedJob" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow rounded-4">
          <div class="modal-header border-0 pb-0 pt-4 px-4">
            <h5 class="modal-title fw-bold">Job Details</h5>
            <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <h4 class="fw-bold mb-4">{{ selectedJob.title }}</h4>
            <div class="row mb-4">
              <div class="col-md-4 mb-4">
                <div class="text-muted small fw-medium text-uppercase mb-1">Salary</div>
                <div class="fw-medium">{{ selectedJob.salary || 'Not specified' }}</div>
              </div>
              <div class="col-md-4 mb-4">
                <div class="text-muted small fw-medium text-uppercase mb-1">Skills</div>
                <div class="fw-medium">{{ selectedJob.skills_required || 'Any' }}</div>
              </div>
              <div class="col-md-4 mb-4">
                <div class="text-muted small fw-medium text-uppercase mb-1">Status</div>
                <div><span class="badge rounded-pill px-3 py-2" :class="statusClass(selectedJob.status)">{{ selectedJob.status }}</span></div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="text-muted small fw-medium text-uppercase mb-1">Posted On</div>
                <div class="fw-medium">{{ new Date(selectedJob.created_at).toLocaleDateString() }}</div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="text-muted small fw-medium text-uppercase mb-1">Deadline</div>
                <div class="fw-medium text-danger">{{ selectedJob.deadline ? new Date(selectedJob.deadline).toLocaleString() : 'No deadline' }}</div>
              </div>
            </div>
            <div class="mb-2">
              <div class="text-muted small fw-medium text-uppercase mb-2">Description</div>
              <p style="white-space: pre-wrap;">{{ selectedJob.description }}</p>
            </div>
          </div>
          <div class="modal-footer border-0 pt-0 pb-4 px-4">
            <button type="button" class="btn btn-light fw-medium rounded-pill px-4" @click="showDetailsModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="py-3 px-4 fw-medium text-muted border-0">Job Details</th>
              <th class="py-3 fw-medium text-muted border-0">Status</th>
              <th class="py-3 fw-medium text-muted border-0">Dates</th>
              <th class="py-3 text-end px-4 fw-medium text-muted border-0">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in jobs" :key="job.id">
              <td class="px-4 py-3 border-0 border-bottom">
                <div class="fw-bold text-dark fs-6">{{ job.title }}</div>
                <div class="text-muted small d-flex gap-2 mt-1 align-items-center">
                  <span>{{ job.salary || 'No salary info' }}</span>
                  <span>&bull;</span>
                  <span class="text-truncate" style="max-width: 200px;">{{ job.skills_required || 'No specific skills' }}</span>
                </div>
              </td>
              <td class="py-3 border-0 border-bottom">
                <span class="badge rounded-pill px-3 py-2 fw-medium" :class="statusClass(job.status)">{{ job.status }}</span>
              </td>
              <td class="py-3 border-0 border-bottom">
                <div class="small mb-1">
                  <span class="text-muted">Posted:</span> <span class="fw-medium">{{ new Date(job.created_at).toLocaleDateString() }}</span>
                </div>
                <div class="small">
                  <span class="text-muted">Deadline:</span> <span class="fw-medium text-danger">{{ job.deadline ? new Date(job.deadline).toLocaleDateString() : 'None' }}</span>
                </div>
              </td>
              <td class="text-end px-4 py-3 border-0 border-bottom">
                <div class="d-flex justify-content-end gap-2 align-items-center">
                  <button @click="viewDetails(job)" class="btn btn-sm btn-light rounded-3 px-2 py-1 fw-medium text-primary shadow-sm border" title="View Details">
                    <Eye :size="16" />
                  </button>
                  <button @click="openEditModal(job)" class="btn btn-sm btn-light rounded-3 px-2 py-1 fw-medium text-secondary shadow-sm border" title="Edit">
                    <Edit :size="16" />
                  </button>
                  <button @click="deleteJob(job.id)" class="btn btn-sm btn-light rounded-3 px-2 py-1 fw-medium text-danger shadow-sm border" title="Delete">
                    <Trash2 :size="16" />
                  </button>
                  <button v-if="job.status === 'Approved'" @click="updateStatus(job.id, 'Closed')" class="btn btn-sm btn-light rounded-3 px-2 py-1 fw-medium text-warning shadow-sm border" title="Close Job">
                    <X :size="16" />
                  </button>
                  <button v-if="job.status === 'Closed'" @click="updateStatus(job.id, 'Approved')" class="btn btn-sm btn-light rounded-3 px-2 py-1 fw-medium text-success shadow-sm border" title="Re-open Job">
                    <CheckCircle :size="16" />
                  </button>
                  <router-link :to="`/company/applications?job_id=${job.id}`" class="btn btn-sm btn-primary rounded-3 px-3 py-1 fw-medium shadow-sm border-0 d-flex align-items-center gap-1 ms-1" title="View Applications">
                    <Users :size="16" />
                    Applicants
                  </router-link>
                </div>
              </td>
            </tr>
            <tr v-if="jobs.length === 0">
              <td colspan="4" class="text-center py-5 text-muted border-0">
                <Briefcase class="mb-3 opacity-50" :size="48" />
                <h5 class="fw-bold">No jobs posted yet</h5>
                <p>Click "Post New Job" to get started.</p>
              </td>
            </tr>
          </tbody>
        </table>
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
      search: '',
      showModal: false,
      showDetailsModal: false,
      isEditing: false,
      selectedJob: null,
      jobForm: {
        id: null,
        title: '',
        description: '',
        salary: '',
        skills_required: '',
        deadline: ''
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
        this.jobs = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    openCreateModal() {
      this.isEditing = false;
      this.jobForm = { id: null, title: '', description: '', salary: '', skills_required: '', deadline: '' };
      this.showModal = true;
    },
    openEditModal(job) {
      this.isEditing = true;
      let deadlineStr = '';
      if (job.deadline) {
        const d = new Date(job.deadline);
        deadlineStr = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      }
      this.jobForm = {
        id: job.id,
        title: job.title,
        description: job.description,
        salary: job.salary,
        skills_required: job.skills_required,
        deadline: deadlineStr
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    viewDetails(job) {
      this.selectedJob = job;
      this.showDetailsModal = true;
    },
    async saveJob() {
      try {
        const payload = { ...this.jobForm };
        if (payload.deadline) {
            payload.deadline = new Date(payload.deadline).toISOString();
        } else {
            payload.deadline = null;
        }

        if (this.isEditing) {
          await api.put(`/company/jobs/${this.jobForm.id}`, payload);
          alert('Job updated successfully. All applied students have been notified via email.');
        } else {
          await api.post('/company/jobs', payload);
          alert('Job created successfully. It will be visible to students once approved by the admin.');
        }
        this.closeModal();
        this.fetchJobs();
      } catch (error) {
        console.error('Error saving job:', error);
        alert('Failed to save job: ' + (error.response?.data?.msg || error.message));
      }
    },
    async deleteJob(id) {
      if (confirm('Are you sure you want to delete this job? This cannot be undone.')) {
        try {
          await api.delete(`/company/jobs/${id}`);
          this.fetchJobs();
        } catch (error) {
          console.error('Error deleting job:', error);
        }
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
      if (status === 'Approved') return 'bg-success bg-opacity-10 text-success';
      if (status === 'Pending') return 'bg-warning bg-opacity-10 text-warning';
      if (status === 'Closed') return 'bg-secondary bg-opacity-10 text-secondary';
      if (status === 'Rejected') return 'bg-danger bg-opacity-10 text-danger';
      return 'bg-primary bg-opacity-10 text-primary';
    }
  }
}
</script>
