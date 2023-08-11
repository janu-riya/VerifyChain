<template>
    <v-app notary>

      <v-app-bar app color="#3498db">
         <img class="mr-3" :src="require('../assets/blockedge-logo.svg')" height="40"/>
      <v-spacer></v-spacer>

      &emsp; &emsp;
      
      <v-spacer></v-spacer>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon

            v-on="on"
          >
            <v-icon color="black">mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list color="#3498db">

<v-list-item @click="profile()">
  <v-divider></v-divider>
  <v-list-item-action>
    <v-icon color="black">mdi-account</v-icon>
  </v-list-item-action>
  &emsp; &emsp;
  <v-list-item-title style="color:black"> Profile</v-list-item-title>
</v-list-item>
</v-list>
        <v-list color="#3498db">

          
          <v-list-item @click="logout()">
            <v-divider></v-divider>
            <v-list-item-action>
              <v-icon color="black">mdi-logout</v-icon>
            </v-list-item-action>
            &emsp; &emsp;
            <v-list-item-title style="color:black">Logout</v-list-item-title>
          </v-list-item>
        </v-list>

      </v-menu>
    </v-app-bar>
        <v-main>
            <Nuxt/>
        </v-main>
    </v-app>
</template>
<script>
export default {
  name:'SuperAdmin_layout',
 
  data: () => {
    return {
      drawer: false,
    };
  },
    methods:{
        async logout (){
          console.log('logout');
          this.$router.push('/SuperAdminLogin');

        },
        async home(){
          this.$router.push('/')
        },
       
    }
}
</script>
