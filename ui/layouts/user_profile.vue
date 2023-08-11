<template>

    <v-app>
      <v-app-bar app color="#3498db">
         <img class="mr-3" :src="require('../assets/blockedge-logo.svg')" height="40"/>
      <v-spacer></v-spacer>
      &ensp; &ensp; &ensp;
      <v-toolbar-title style="color: black;">User Profile</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
        <v-btn text style="color: black;width: 100px;" @click="logout()">Logout</v-btn>

    </v-app-bar>
    <v-main>
      <Nuxt/>
    </v-main>
    <v-footer
      color="#3498db"
      dark
    >
      <v-row
        justify="center"
        class="my-4 text-center"
      >
        <v-col cols="12" style="color:black"
          >Copyright @ Securekloud Technologies Ltd {{ new Date().getFullYear() }}</v-col
        >
        <v-col cols="12">
          <v-btn style="width: 5%; color:black"
            v-for="icon in icons"
            :key="icon"
            text
            dark
          >
            <v-icon>{{ icon }}</v-icon>
          </v-btn>
        </v-col>
        <v-col
          cols="12"
          class="align-center" style="color:black"
          >&copy; 2023 VerifiEdge</v-col
        >
      </v-row>
    </v-footer>
  </v-app>

</template>

  <script >
  export default {
    name:'user_profile',
    async mounted () {
    this.$vuetify.theme.dark = false
  },
  data() {
    return {
      drawer: false,
    };
  },  
  methods: {
    async logout() {

      localStorage.removeItem('access_token');
      console.log("removed")
        // this.$router.push("/notary")

    }
  }

  }
</script>
