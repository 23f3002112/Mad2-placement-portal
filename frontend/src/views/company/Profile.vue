<template>
  <div class="card">
    <div class="card-header">
      <h4>Company Profile</h4>
    </div>
    <div class="card-body">
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Company Name</label>
          <input type="text" class="form-control" v-model="profile.name" disabled>
        </div>
        <div class="mb-3">
          <label class="form-label">Industry</label>
          <input type="text" class="form-control" v-model="profile.industry">
        </div>
        <div class="mb-3">
          <label class="form-label">Location</label>
          <input type="text" class="form-control" v-model="profile.location">
        </div>
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea class="form-control" v-model="profile.description" rows="4"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Profile</button>
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
        description: ''
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
