<template>
  <v-container>
    <v-container v-if="show">
      <v-card class="mx-auto my-12"
    max-width="700">
    <table class="styled-table">
      <thead>
        <tr>
          <th class="styled-table-header">Name</th>
          <th class="styled-table-header">Email</th>
          <th class="styled-table-header">Profile</th>
          <th class="styled-table-header">Approve</th>

        </tr>
      </thead>
      <tbody>
        <tr  v-for="request in paginatedRequests"
        :key="request.email">
          <td>{{ request.name }}</td>
          <td>{{ request.email }}</td>
          <td>
            <v-btn text color="primary" @click="view(request.email)">View</v-btn>
          </td>
          <td>
            <v-btn icon @click="approve(request.email)">
              <v-icon color="green">mdi-check</v-icon>
            </v-btn>
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
      <h2 class="text-center" text color="blue lighten-1">No Profiles</h2>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "NotaryInProgress",

  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      profiles: [],
      requests: {},
      count: {},
      notary_email: null,
      notary_name: null,
      wallet: 0,
      show: false,
      hide: false
    };
  },

  async mounted() {
    this.$vuetify.theme.dark = false;
    await this.fetchRequests();
  },

  computed: {
    totalPages() {
      return Math.ceil(this.requests.length / this.pageSize);
    },
    paginatedRequests() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.requests.slice(startIndex, endIndex);
    },
  },

  methods: {
    async fetchRequests() {
      try {
        const response = await this.$axios.get("http://127.0.0.1:8000/inprogressuser");
        this.requests = response.data.list;
        this.show = this.requests.length > 0;
        this.hide = !this.show;
      } catch (error) {
        console.error(error);
      }
    },

    changePage(page) {
      this.currentPage = page;
    },

    async view(email) {
      this.$storage.setUniversal("user_email", email);
      this.$router.push("/userprofile");
    },

    async approve(email) {
      try {
        const url = "http://127.0.0.1:8000/inprogress_verified";
        const data = {
          email: email,
        };
        const response = await this.$axios.post(url, data);
        window.location.reload();
      } catch (error) {
        console.error(error);
      }

      let rurl = "http://127.0.0.1:8000/send_rejection_email"
        let rdata={
          email: email,
          email_subject: "Approval Mail",
          email_body: `
          Dear Applicant,

          We are here to inform you that your Data has approved by the notary.

          We appreciate your interest in our services and your effort in applying. Thank you for considering us.

          With Regards,

          VerifiEdge

          `
        }
        let nres = await this.$axios.post(rurl, rdata)
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