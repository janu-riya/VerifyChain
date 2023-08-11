<template>
  <v-container>
    <v-container v-if="show">
      <h2 class="text-center styled-no-profiles" text color="blue lighten-1">Approved Profiles</h2>
      <v-card class="mx-auto my-12" max-width="700">
        <table class="styled-table">
          <thead>
            <tr>
              <th class="styled-table-header">Name</th>
              <th class="styled-table-header">Email</th>
              <th class="styled-table-header">Profile</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="profile in paginatedProfiles" :key="profile.email">
              <td>{{ profile.name }}</td>
              <td>{{ profile.email }}</td>
              <td>
                <v-btn text color="primary" @click="view(profile.email)">View</v-btn>
              </td>
            </tr>
          </tbody>
        </table>
        <v-container class="text-center">
          <v-pagination
            v-model="currentPage"
            :total-visible="5"
            :length="totalPages"
            @input="changePage"
          ></v-pagination>
        </v-container>
      </v-card>
    </v-container>
    <v-container v-if="hide">
      <h2 class="text-center styled-no-profiles" text color="blue lighten-1">No Profiles yet approved</h2>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "Approveprofiles",

  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      profiles: [],
      requests: {},
      notary_email: null,
      notary_name: null,
      wallet: 0,
      show: false,
      hide: false,
    };
  },

  async mounted() {
    this.$vuetify.theme.dark = false;
    await this.fetchProfiles();
  },

  computed: {
    totalPages() {
      return Math.ceil(this.profiles.length / this.pageSize);
    },
    paginatedProfiles() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.profiles.slice(startIndex, endIndex);
    },
  },

  methods: {
    async fetchProfiles() {
      try {
        const response = await this.$axios.get("http://127.0.0.1:8000/verifiedusers");
        this.profiles = response.data.list;
        this.show = this.profiles.length > 0;
        this.hide = !this.show;
      } catch (error) {
        console.error(error);
      }
    },

    changePage(page) {
      this.currentPage = page;
    },

    async view(email){
        this.$storage.setUniversal('search_email', email)
        this.$router.push('/User_companyprofile')
      },
  },
};
</script>
<style scoped>
.styled-table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  border: 1px solid #ccc;
}

.styled-table th,
.styled-table td {
  padding: 10px;
  text-align: center;
}

.styled-table-header {
  background-color: #f0f0f0;
}

.styled-table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.styled-no-profiles {
  color: darkblue;
}

/* Adjust the button color */
.v-btn.primary {
  color: #fff;
  background-color: #3498db;
}
</style>