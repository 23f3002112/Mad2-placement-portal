<template>
  <div class="mt-4">
    <h2>Manage Students</h2>
    <div class="mb-3">
      <input type="text" v-model="search" @input="fetchStudents" class="form-control" placeholder="Search by name...">
    </div>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Education</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td>{{ student.id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.education }}</td>
            <td>{{ student.email }}</td>
            <td>
              <span class="badge" :class="student.is_active ? 'bg-success' : 'bg-danger'">
                {{ student.is_active ? 'Active' : 'Deactivated' }}
              </span>
            </td>
            <td>
              <button @click="blacklistStudent(student.id)" class="btn btn-sm" :class="student.is_active ? 'btn-danger' : 'btn-info'">
                {{ student.is_active ? 'Blacklist' : 'Activate' }}
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
      students: [],
      search: ''
    }
  },
  mounted() {
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await api.get(`/admin/students?search=${this.search}`);
        this.students = response.data;
      } catch (error) {
        console.error('Error fetching students:', error);
      }
    },
    async blacklistStudent(id) {
      if (confirm('Are you sure you want to change the status of this student?')) {
        try {
          await api.post(`/admin/students/${id}/blacklist`);
          this.fetchStudents();
        } catch (error) {
          console.error(error);
        }
      }
    }
  }
}
</script>
