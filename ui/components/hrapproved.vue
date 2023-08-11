<template>
    <v-container>
     <v-container>
        <h2 class="text-center" style="color: darkblue;">Approved Profiles</h2>
     </v-container>
     <v-card
    class="mx-auto pa-2"
    style="width: 80%;"
  >
    <v-list density="compact">
      <v-list-item
        v-for="profile in profiles"
        :key="profile.email"
        :value="profile.email"
        active-color="primary"
      >
        <v-list-item-subtitle v-text="profile.user_email"></v-list-item-subtitle>
        <v-list-item-title v-text="profile.status"></v-list-item-title>
        <v-btn icon @click="view(profile.user_email)"><v-icon color="blue lighten-1">mdi-card-account-details-outline</v-icon></v-btn>
      </v-list-item>
    </v-list>
  </v-card>
</v-container>
</template>
<script>
export default{
    name :"hrapproved",
    async mounted(){
        this.hr_email= await this.$storage.getUniversal('hrmail');
        let url = "http://127.0.0.1:8000/hr/approved"
        let res = await this.$axios.get(url,{params :{email:this.hr_email}});
        this.profiles = res.data
        console.log(this.profiles)
    },
    data:()=>({
        profiles:[],
        hr_email:""
    }),
    methods:{
        async view(email){
            this.$storage.setUniversal('user_email',email)
            this.$storage.setUniversal('hrlogin',1)
            this.$router.push('/companyprofile')
        }
    }
}
</script>
