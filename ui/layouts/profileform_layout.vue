<template>
  <v-app userprofile>
      <v-app-bar app  color="#3498db">
        <img class="mr-3" :src="require('../assets/blockedge-logo.svg')" height="40"/>
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
      <v-col cols="12" style="width: 10%;">
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
<script>
export default {
name:'profileform_layout',
data: () => {
  return {
    icons: [
      'mdi-facebook',
      'mdi-twitter',
      'mdi-instagram',
      'mdi-youtube',
    ],
  };
},
  methods:{
      async logout (){
        this.$router.push('/user')

      }
  }
}
</script>
