<template>


    <v-container style="width: 80%; ">
  
          <v-container>
            <v-row>
              <v-col style="padding-left: 4%;">
                <h3 class="text-title-1">Address</h3>
                <h3 class="text-subtitle-1">{{ pdata.houseNo }}, {{ pdata.street }}</h3>
                <h3 class="text-subtitle-1">{{ pdata.region }} - {{ pdata.zipcode }} </h3>
                <h3 class="text-subtitle-1">{{ pdata.state }}, {{ pdata.country }}</h3>


  
              </v-col>
  
  
            </v-row>
          </v-container>
  
  
    </v-container>
  </template>
  
  <script>
  export default{
  name: 'userprofile',
  async mounted (){
    this.$vuetify.theme.dark =false;
    this.email = this.$storage.getUniversal('search_email')
    let url = "http://127.0.0.1:8000/personal"
    let res = await this.$axios.get(url,{params:{ email :this.email}});
    this.pdata=res.data
    console.log(this.pdata)
  
  
  },
  data: () =>({
    email:"",
    pdata :{},
  
  }),
  }
  </script>
  