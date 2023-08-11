<template>
  <v-container v-if="isAuthenticated">
    <v-col>
      <v-row rows="4">
        <upload/>
        </v-row>
      </v-col>
  </v-container>
</template>
<script>
export default{
    layout:"hr_layout",
    async mounted(){
      const accessToken = localStorage.getItem('access_token');
    this.isAuthenticated = !!accessToken;
    },
    data: () => ({
      isAuthenticated: false
    })

}
</script>