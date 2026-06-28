<template>
  <div class="card">
    <div class="card-header">
      <h4>My Profile</h4>
    </div>
    <div class="card-body">
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input type="text" class="form-control" v-model="profile.name" disabled>
        </div>
        <div class="mb-3">
          <label class="form-label">Education</label>
          <input type="text" class="form-control" v-model="profile.education" placeholder="e.g. B.Tech Computer Science">
        </div>
        <div class="mb-3">
          <label class="form-label">Skills</label>
          <input type="text" class="form-control" v-model="profile.skills" placeholder="e.g. Python, Java, VueJS">
        </div>
        <div class="mb-3">
          <label class="form-label">Resume URL</label>
          <input type="url" class="form-control" v-model="profile.resume_url" placeholder="https://link-to-your-resume.com">
        </div>
        <div class="mb-3">
          <label class="form-label">Experience</label>
          <textarea class="form-control" v-model="profile.experience" rows="4" placeholder="Briefly describe any past internships or projects..."></textarea>
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
        education: '',
        skills: '',
        resume_url: '',
        experience: ''
      }
    }
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await api.get('/student/profile');
        this.profile = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        await api.put('/student/profile', this.profile);
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
  }
}
</script>
