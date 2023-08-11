<template>
    <v-container>
      <v-container v-if="show">
      <v-card
        class="mx-auto pa-2"
        style="width: 80%;"
      >
        <v-list density="compact">
          <v-list-item
            v-for="info in infos"
            :key="info.email"
            :value="info.email"
            active-color="primary"
          >
            <v-list-item-title v-text="info.name"></v-list-item-title>
            <v-list-item-subtitle v-text="info.company_mail"></v-list-item-subtitle>
            <v-btn icon @click="view(info.company_mail)"><v-icon color="indigo darken-4">mdi-card-account-details-outline</v-icon></v-btn>

          </v-list-item>
        </v-list>
        </v-card>
      </v-container>
      <v-container v-if="hide">
        <h2 class="text-center" text color="blue lighten-1">No Requests </h2><br /><br/>
      </v-container>
  
      </v-container>
  </template>
  
  <script>
  export default{
      name :"CompanyApproved",
    
      async mounted(){
          this.$vuetify.theme.dark=false;
          let url = "http://127.0.0.1:8000/company/verified"
          let res = await this.$axios.get(url)
          this.infos = res.data.list
  
          if(this.infos == false){
            this.hide = true
            this.show = false
          }
          else{
            this.show = true
            this.hide = false
          }
      },
  
      data:() =>({
        infos: [],
        wallet:0,
        show: false,
        hide:false
      }),
      methods:{
        async home(){
          this.$router.push("/");
        },
  
        async view(company_mail){
            this.$storage.setUniversal('company_email',company_mail)
          
          this.$router.push("/companyyprofile")
        },
    
      }
  
    }
  </script>
  