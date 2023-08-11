<template>
  <v-container>
    <v-container v-if="show">
    <v-card
      class="mx-auto pa-2"
      style="width: 80%;"
    >
      <v-list density="compact">
        <v-list-item
          v-for="data in datas"
          :key="data.email"
          :value="data.email"
          active-color="primary"
        >
          <v-list-item-title v-text="data.name"></v-list-item-title>
          <v-list-item-subtitle v-text="data.email"></v-list-item-subtitle>
          <v-btn icon @click="view(data.email)"><v-icon color="blue lighten-1">mdi-card-account-details-outline</v-icon></v-btn>
        
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
    name :"NotaryyApproved",
    
    async mounted(){
        this.$vuetify.theme.dark=false;
        let url = "http://127.0.0.1:8000/notary/verified"
        let res = await this.$axios.get(url)
        this.datas = res.data.list

        if(this.datas == false){
          this.hide = true
          this.show = false
        }
        else{
          this.show = true
          this.hide = false
        }
    },

    data:() =>({
      datas: [],
      wallet:0,
      show: false,
      hide:false
    }),
    methods:{
      async home(){
        this.$router.push("/");
      },

      async view(email){
          this.$storage.setUniversal('notary_email',email)
        
        this.$router.push("/NotaryyProfile")
      },
  
    }

  }
</script>
