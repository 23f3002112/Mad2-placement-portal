<template>
  <div class="landing-page">
    <div class="hero-section position-relative d-flex align-items-center justify-content-center text-center">
      <div class="hero-content z-index-2">
        <h1 class="display-3 fw-bold mb-4">
          <span class="text-dark">Job</span><span class="text-primary">Finder</span> Find what's next
        </h1>
        <p class="lead text-muted mb-5 max-w-700 mx-auto">
          Discover your next career move, connect with top companies, and unlock your potential.
        </p>
        <div class="d-flex justify-content-center gap-3">
          <router-link to="/register?role=student" class="btn btn-primary btn-lg rounded-pill px-4 py-2 fw-semibold shadow-sm">I'm looking for a job</router-link>
          <router-link to="/register?role=company" class="btn btn-outline-dark btn-lg rounded-pill px-4 py-2 fw-semibold shadow-sm bg-white">I'm hiring</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing-page {
  min-height: calc(100vh - 80px);
  background-color: #fbfbfe; /* Very light, soft background */
  overflow: hidden;
}

.hero-section {
  height: calc(100vh - 80px);
  width: 100%;
}

.z-index-2 {
  z-index: 2;
  position: relative;
  background: rgba(251, 251, 254, 0.85);
  padding: 4rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.z-index-1 {
  z-index: 1;
}

.max-w-700 {
  max-width: 700px;
}



/* Adjust header specific styles */
.text-primary {
  color: #ff3e6c !important; /* Wellfound-like red accent */
}
</style>
