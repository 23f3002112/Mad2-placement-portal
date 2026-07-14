<template>
  <div class="mt-4">
    <h2>Search Results for "{{ searchQuery }}"</h2>
    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else class="mt-4">
      <div v-if="!hasResults && searchQuery" class="alert alert-info">
        No results found for "{{ searchQuery }}".
      </div>
      
      <!-- Students -->
      <div v-if="results.students.length > 0" class="mb-5">
        <h4>Students</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Education</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in results.students" :key="student.id">
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.education }}</td>
                <td>{{ student.email }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Companies -->
      <div v-if="results.companies.length > 0" class="mb-5">
        <h4>Companies</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Industry</th>
                <th>Location</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in results.companies" :key="company.id">
                <td>{{ company.id }}</td>
                <td>{{ company.name }}</td>
                <td>{{ company.industry }}</td>
                <td>{{ company.location }}</td>
                <td>
                  <span class="badge" :class="company.is_approved ? 'bg-success' : 'bg-warning'">
                    {{ company.is_approved ? 'Approved' : 'Pending' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Jobs -->
      <div v-if="results.jobs.length > 0" class="mb-5">
        <h4>Placement Drives</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Company Name</th>
                <th>Job Title</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="job in results.jobs" :key="job.id">
                <td>{{ job.id }}</td>
                <td>{{ job.company_name }}</td>
                <td>{{ job.title }}</td>
                <td>
                  <span class="badge" :class="statusClass(job.status)">
                    {{ job.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
      searchQuery: '',
      results: {
        companies: [],
        students: [],
        jobs: []
      },
      loading: false
    }
  },
  computed: {
    hasResults() {
      return this.results.companies.length > 0 || 
             this.results.students.length > 0 || 
             this.results.jobs.length > 0;
    }
  },
  mounted() {
    this.searchQuery = this.$route.query.search || '';
    if (this.searchQuery) {
      this.fetchResults();
    }
  },
  watch: {
    '$route.query.search': function(newVal) {
      this.searchQuery = newVal || '';
      if (this.searchQuery) {
        this.fetchResults();
      } else {
        this.results = { companies: [], students: [], jobs: [] };
      }
    }
  },
  methods: {
    async fetchResults() {
      this.loading = true;
      try {
        const response = await api.get(`/admin/search?q=${this.searchQuery}`);
        this.results = response.data;
      } catch (error) {
        console.error('Error fetching global search:', error);
      } finally {
        this.loading = false;
      }
    },
    statusClass(status) {
      if (status === 'Approved') return 'bg-success';
      if (status === 'Pending') return 'bg-warning';
      if (status === 'Rejected') return 'bg-danger';
      return 'bg-secondary';
    }
  }
}
</script>
