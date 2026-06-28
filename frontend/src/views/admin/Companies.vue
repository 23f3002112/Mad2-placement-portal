<template>
  <div class="mt-4">
    <h2>Manage Companies</h2>
    <div class="mb-3">
      <input type="text" v-model="search" @input="fetchCompanies" class="form-control" placeholder="Search by name or industry...">
    </div>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.id }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.industry }}</td>
            <td>{{ company.location }}</td>
            <td>
              <span class="badge" :class="company.is_approved ? 'bg-success' : 'bg-warning'">
                {{ company.is_approved ? 'Approved' : 'Pending' }}
              </span>
              <span class="badge ms-1" :class="company.is_active ? 'bg-info' : 'bg-danger'">
                {{ company.is_active ? 'Active' : 'Deactivated' }}
              </span>
            </td>
            <td>
              <button v-if="!company.is_approved" @click="approveCompany(company.id)" class="btn btn-sm btn-success me-1">Approve</button>
              <button v-if="!company.is_approved" @click="rejectCompany(company.id)" class="btn btn-sm btn-danger">Reject</button>
              <button v-if="company.is_approved" @click="blacklistCompany(company.id)" class="btn btn-sm" :class="company.is_active ? 'btn-danger' : 'btn-info'">
                {{ company.is_active ? 'Blacklist' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      companies: [],
      search: ''
    }
  },
  mounted() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      try {
        const response = await api.get(`/admin/companies?search=${this.search}`);
        this.companies = response.data;
      } catch (error) {
        console.error('Error fetching companies:', error);
      }
    },
    async approveCompany(id) {
      if (confirm('Are you sure you want to approve this company?')) {
        try {
          await api.post(`/admin/companies/${id}/approve`);
          this.fetchCompanies();
        } catch (error) {
          console.error(error);
        }
      }
    },
    async rejectCompany(id) {
      if (confirm('Are you sure you want to reject and remove this company?')) {
        try {
          await api.post(`/admin/companies/${id}/reject`);
          this.fetchCompanies();
        } catch (error) {
          console.error(error);
        }
      }
    },
    async blacklistCompany(id) {
      if (confirm('Are you sure you want to change the status of this company?')) {
        try {
          await api.post(`/admin/companies/${id}/blacklist`);
          this.fetchCompanies();
        } catch (error) {
          console.error(error);
        }
      }
    }
  }
}
</script>
