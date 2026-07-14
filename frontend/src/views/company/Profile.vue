<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-header bg-white border-0 pt-4 pb-0 px-4">
      <h4 class="fw-bold mb-0">Company Profile</h4>
    </div>
    <div class="card-body p-4">
      <form @submit.prevent="updateProfile">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Company Name</label>
            <input type="text" class="form-control" v-model="profile.name" disabled>
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Industry</label>
            <input type="text" class="form-control" v-model="profile.industry" placeholder="e.g. Technology, Finance">
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Location</label>
            <input type="text" class="form-control" v-model="profile.location" placeholder="e.g. San Francisco, CA">
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Website</label>
            <input type="url" class="form-control" v-model="profile.website" placeholder="https://www.example.com">
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Employee Count</label>
            <select class="form-select" v-model="profile.employee_count">
              <option value="">Select range</option>
              <option value="1-10">1-10</option>
              <option value="11-50">11-50</option>
              <option value="51-200">51-200</option>
              <option value="201-500">201-500</option>
              <option value="501-1000">501-1000</option>
              <option value="1001+">1001+</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-medium">Founded Year</label>
            <input type="number" class="form-control" v-model="profile.founded_year" placeholder="e.g. 2010" min="1800" max="2100">
          </div>
          <div class="col-md-12 mb-3">
            <label class="form-label fw-medium">Contact Email</label>
            <input type="email" class="form-control" v-model="profile.contact_email" placeholder="contact@company.com">
          </div>
          <div class="col-md-12 mb-4">
            <label class="form-label fw-medium">Description</label>
            <textarea class="form-control" v-model="profile.description" rows="5" placeholder="Tell us about your company..."></textarea>
          </div>
        </div>
        <button type="submit" class="btn btn-primary px-4 fw-medium">Update Profile</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      profile: {
        name: '',
        industry: '',
        location: '',
        description: '',
        website: '',
        employee_count: '',
        founded_year: '',
        contact_email: ''
      }
    }
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await api.get('/company/profile');
        this.profile = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        await api.put('/company/profile', this.profile);
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
  }
}
</script>
