<template>
    <v-app notary>

      <v-app-bar app color="#3498db">
         <img class="mr-3" :src="require('../assets/blockedge-logo.svg')" height="40"/>
      <v-spacer></v-spacer>
      
      <v-spacer/>
      
      <v-spacer></v-spacer>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon

            v-on="on"
          >
            <v-icon  color="black">mdi-account-circle</v-icon>
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
          <v-list-item @click="user()">
            <v-divider></v-divider>
            <v-list-item-action>
              <v-icon color="black">mdi-account</v-icon>
            </v-list-item-action>
            &emsp; &emsp;
            <v-list-item-title style="color:black"> Users</v-list-item-title>
          </v-list-item>
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
  name:'notary_layout',
  async mounted(){
    let nurl ="http://127.0.0.1:8000/notary"
        this.email = this.$storage.getUniversal('notaryemail')
        let nres = await this.$axios.get(nurl,{
          params :{
            email : this.email
          }
        });
        this.notary_name = nres.data.name
  },
  data: () => {
    return {
      drawer: false,
      email:""
    };
  },
    methods:{
        async logout (){

          let url = "http://127.0.0.1:8000/notary/last_login"
          let ndata={
            email:this.email
          }
          let nres =  await this.$axios.post(url, ndata)
          localStorage.removeItem('access_token');

          console.log('logout');
          this.$router.push('/notarysignin');

        },
        async home(){
          this.$router.push('/notary')
        },
        async profile(){
        this.$router.push('/notary_profile')
      },
       async user(){
        this.$router.push('/notary')
       }
    }
}
</script>
