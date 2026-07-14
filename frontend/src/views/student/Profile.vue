<template>
  <div>
    <h3 class="fw-bold mb-4">Edit your profile</h3>
    
    <!-- Tabs -->
    <div class="d-flex border-bottom mb-4 gap-4">
      <div 
        class="pb-3 cursor-pointer fw-medium position-relative" 
        :class="activeTab === 'Overview' ? 'text-dark' : 'text-muted'"
        @click="activeTab = 'Overview'">
        Overview
        <div v-if="activeTab === 'Overview'" class="position-absolute bottom-0 start-0 w-100 bg-dark" style="height: 2px;"></div>
      </div>
      <div 
        class="pb-3 cursor-pointer fw-medium position-relative" 
        :class="activeTab === 'Profile' ? 'text-dark' : 'text-muted'"
        @click="activeTab = 'Profile'">
        Profile
        <div v-if="activeTab === 'Profile'" class="position-absolute bottom-0 start-0 w-100 bg-dark" style="height: 2px;"></div>
      </div>
      <div 
        class="pb-3 cursor-pointer fw-medium position-relative" 
        :class="activeTab === 'Resume' ? 'text-dark' : 'text-muted'"
        @click="activeTab = 'Resume'">
        Resume / CV
        <div v-if="activeTab === 'Resume'" class="position-absolute bottom-0 start-0 w-100 bg-dark" style="height: 2px;"></div>
      </div>
    </div>

    <div>
      <!-- Overview Tab -->
      <div v-if="activeTab === 'Overview'">
        <h4 class="fw-bold mb-4">What recruiters will see</h4>
        <div class="card border shadow-sm rounded-3">
          <div class="card-body p-4 p-md-5">
            <div class="d-flex align-items-start gap-4 mb-4">
              <div class="rounded-circle bg-light d-flex align-items-center justify-content-center border overflow-hidden" style="width: 72px; height: 72px;">
                <img v-if="profile.photo_url" :src="profile.photo_url" style="width: 100%; height: 100%; object-fit: cover;">
                <svg v-else width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              </div>
              <div>
                <h3 class="fw-bold mb-1">{{ profile.name }}</h3>
                <p class="text-muted mb-2 small" v-if="profile.location">{{ profile.location }}</p>
                <span class="badge bg-light text-dark border fw-medium px-3 py-2 rounded-pill">Active today</span>
              </div>
            </div>

            <div class="mb-4" v-if="profile.experience">
              <h6 class="text-muted fw-medium small mb-2">Bio</h6>
              <div class="text-dark" style="white-space: pre-wrap;">{{ profile.experience }}</div>
            </div>

            <div class="mb-4" v-if="profile.education">
              <h6 class="text-muted fw-medium small mb-2">Education</h6>
              <div class="fw-bold text-dark">{{ profile.education }}</div>
            </div>

            <div class="mb-4" v-if="profile.skills">
              <h6 class="text-muted fw-medium small mb-2">Skills</h6>
              <div class="text-dark">{{ profile.skills }}</div>
            </div>
            
            <div class="mb-4" v-if="profile.resume_url">
              <h6 class="text-muted fw-medium small mb-2">Resume / CV</h6>
              
              <a v-if="profile.resume_url.includes('/static/uploads/')" :href="'http://127.0.0.1:5000/api/student/download_resume/' + profile.resume_url.split('/').pop()" class="btn btn-outline-primary btn-sm d-inline-flex align-items-center gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                Download Resume
              </a>

              <a v-else :href="profile.resume_url" target="_blank" class="btn btn-outline-primary btn-sm d-inline-flex align-items-center gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                View Resume Link
              </a>
            </div>

            <div v-if="profile.linkedin || profile.github">
              <h6 class="text-muted fw-medium small mb-2">Social Profiles</h6>
              <div class="d-flex flex-column gap-2">
                <a v-if="profile.linkedin" :href="profile.linkedin" target="_blank" class="text-decoration-none text-primary fw-medium small">LinkedIn</a>
                <a v-if="profile.github" :href="profile.github" target="_blank" class="text-decoration-none text-dark fw-medium small">GitHub</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Tab -->
      <div v-if="activeTab === 'Profile'">
        <div class="card border shadow-sm rounded-3">
          <div class="card-body p-4 p-md-5">
            <form @submit.prevent="updateProfile">
              <div class="row mb-5">
                <div class="col-md-3 mb-3 mb-md-0">
                  <h6 class="fw-bold mb-1">
                    About
                  </h6>
                  <p class="text-muted small">Tell us about yourself so startups know who you are.</p>
                </div>
                <div class="col-md-9">
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small">Your name*</label>
                    <input type="text" class="form-control" v-model="profile.name" placeholder="Rajeev Patel" required>
                  </div>
                  <div class="mb-4 d-flex align-items-center gap-3">
                    <div class="rounded-circle bg-light d-flex align-items-center justify-content-center border overflow-hidden" style="width: 64px; height: 64px;">
                      <img v-if="profile.photo_url" :src="profile.photo_url" style="width: 100%; height: 100%; object-fit: cover;">
                      <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    </div>
                    <input type="file" class="d-none" ref="photoInput" @change="onPhotoSelected" accept="image/*">
                    <button type="button" class="btn btn-outline-dark fw-medium btn-sm px-3" @click="$refs.photoInput.click()">Upload a new photo</button>
                  </div>
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small">Where are you based?*</label>
                    <input type="text" class="form-control" v-model="profile.location" placeholder="India, India">
                  </div>
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small">Your bio</label>
                    <textarea class="form-control" v-model="profile.experience" rows="4" placeholder="Stanford CS, Full stack generalist; launched a successful Android app, worked at Google"></textarea>
                  </div>
                </div>
              </div>

              <hr class="mb-5">

              <div class="row mb-5">
                <div class="col-md-3 mb-3 mb-md-0">
                  <h6 class="fw-bold mb-1">Social Profiles</h6>
                  <p class="text-muted small">Where can people find you online?</p>
                </div>
                <div class="col-md-9">
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small d-flex align-items-center gap-2">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
                      LinkedIn
                    </label>
                    <input type="url" class="form-control" v-model="profile.linkedin" placeholder="https://linkedin.com/in/username">
                  </div>
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small d-flex align-items-center gap-2">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
                      GitHub
                    </label>
                    <input type="url" class="form-control" v-model="profile.github" placeholder="https://github.com/username">
                  </div>
                </div>
              </div>

              <hr class="mb-5">

              <div class="row mb-5">
                <div class="col-md-3 mb-3 mb-md-0">
                  <h6 class="fw-bold mb-1">Education & Skills</h6>
                  <p class="text-muted small">What schools have you studied at and what are your strengths?</p>
                </div>
                <div class="col-md-9">
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small">Education</label>
                    <input type="text" class="form-control" v-model="profile.education" placeholder="e.g. B.Tech Computer Science">
                  </div>
                  <div class="mb-4">
                    <label class="form-label fw-bold text-dark small">Your Skills</label>
                    <div class="input-group">
                      <span class="input-group-text bg-white text-muted border-end-0"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></span>
                      <input type="text" class="form-control border-start-0 ps-0" v-model="profile.skills" placeholder="e.g. Python, React">
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-dark px-4 py-2 fw-medium">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Resume Tab -->
      <div v-if="activeTab === 'Resume'">
        <div class="card border shadow-sm rounded-3">
          <div class="card-body p-4 p-md-5">
            <div class="row">
              <div class="col-md-5 mb-4 mb-md-0">
                <h5 class="fw-bold mb-2">
                  Upload your recent resume or CV
                </h5>
                <p class="text-muted mb-1">Upload your most up-to-date resume, or provide a link to it.</p>
                <p class="text-muted small">File types: DOC, DOCX, PDF, TXT</p>
              </div>
              <div class="col-md-7">
                <input type="file" class="d-none" ref="resumeInput" @change="onResumeSelected" accept=".doc,.docx,.pdf,.txt">
                <div class="border border-secondary border-dashed rounded-3 p-5 text-center cursor-pointer hover-bg-light transition-all mb-4" @click="$refs.resumeInput.click()">
                  <div class="mb-3">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0056b3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                  </div>
                  <h6 class="text-primary fw-bold mb-0">Upload new file</h6>
                </div>
                
                <div class="mb-3">
                  <label class="form-label fw-bold text-dark small">Or paste a link to your resume (e.g. Google Drive)</label>
                  <div class="input-group">
                    <input type="url" class="form-control" v-model="profile.resume_url" placeholder="https://...">
                    <button class="btn btn-dark fw-medium" type="button" @click="updateProfile">Save Link</button>
                  </div>
                </div>

                <div class="mt-4 text-muted small" v-if="profile.resume_url">
                  Current Resume: 
                  <a v-if="profile.resume_url.includes('/static/uploads/')" :href="'http://127.0.0.1:5000/api/student/download_resume/' + profile.resume_url.split('/').pop()" class="fw-medium text-primary text-decoration-none">
                    Download Uploaded File
                  </a>
                  <a v-else :href="profile.resume_url" target="_blank" class="fw-medium text-primary text-decoration-none">
                    View External Link
                  </a>
                </div>
              </div>
            </div>
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
      activeTab: 'Profile',
      profile: {
        name: '',
        education: '',
        skills: '',
        resume_url: '',
        experience: '',
        photo_url: null,
        location: '',
        linkedin: '',
        github: ''
      }
    }
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    onPhotoSelected(event) {
      const file = event.target.files[0];
      if (file) {
        // Create a local object URL to simulate image upload preview
        this.profile.photo_url = URL.createObjectURL(file);
      }
    },
    async onResumeSelected(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        try {
          const response = await api.post('/student/upload_resume', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          this.profile.resume_url = response.data.resume_url;
          alert('Resume uploaded successfully!');
        } catch (error) {
          console.error('Error uploading resume:', error);
          alert('Failed to upload resume');
        }
      }
    },
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

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
.border-dashed {
  border-style: dashed !important;
  border-width: 2px !important;
}
.hover-bg-light:hover {
  background-color: #f8f9fa;
}
.transition-all {
  transition: all 0.2s ease-in-out;
}
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(0, 0, 139, 0.1);
  border-color: #00008b;
}
</style>
