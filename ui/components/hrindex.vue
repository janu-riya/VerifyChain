<template>
  <v-container>
    
    <v-row>
      <v-col>
        <v-card width="99%">
          <v-container class="text-center">
            <h4>&ensp; Current Login: &ensp; &ensp;{{ pdata.login_date }}</h4>

          </v-container>
        </v-card>
      </v-col>
      <v-col>
        <v-card width="97%">
          <v-container class="text-center">
            <h4 v-if="pdata.last_login">&ensp; Last Login: &ensp;&ensp;{{ pdata.last_login }}</h4>

          </v-container>

        </v-card>
      </v-col>
    </v-row>
    <br><br>
    <v-container class="personalform" >
      <v-form>
        <v-row>
          <v-col cols="12">
            <v-text-field label="Enter Email Address" v-model="email"></v-text-field>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
    <v-container class="text-center">
      <v-btn text color="blue lighten-1" style="color:white" @click="search()">Search</v-btn><br/><br/>

    </v-container>
    <v-container v-if="user_yes" >
      <h2 class="text-center" text color="blue lighten-1"> Profiles</h2><br /><br/>

      <v-card
      class="mx-auto my-12"
      max-width="700"
    >
    <v-list density="compact">
      <v-list-item
      >

      
        <v-list-item-title v-text="users.name"></v-list-item-title>
        <v-list-item-subtitle v-text="users.email"></v-list-item-subtitle>
        <v-btn text color="blue lighten-1" @click="view(users.email)">view</v-btn>
        <!--<v-btn icon @click="approve(profile.email)"><v-icon color="green">mdi-account-check-outline</v-icon></v-btn>&emsp;&emsp;
        <v-btn icon @click="deny(profile.email)"><v-icon color="error">mdi-account-remove-outline</v-icon></v-btn>-->
      </v-list-item>
    </v-list>
    </v-card>
    </v-container>
    <v-container v-if="user_no" >
      <h2 class="text-center" text color="blue lightne-1">No Profiles</h2><br /><br/>
    </v-container>
    

  </v-container>
</template>

<script>
export default {
  name:"hrsearch",
  async mounted(){
        this.$vuetify.theme.dark=false;
        this.company_mail = this.$storage.getUniversal('hrmail')
        let nurl = "http://127.0.0.1:8000/hr"
        let nres = await this.$axios.get(nurl,{params:{ company_mail :this.company_mail}});
        this.pdata = nres.data
        console.log(this.pdata)
    },
    data:() =>({
        email:"",
        login_date:"",
        last_login:"",
        company_mail:"",
        users:[],
        pdata:{},
        user_yes: false,
        user_no: false
    }),
    methods:{

      async fileselect(event){
        this.file=event
      },
      async search(){
        let url = "http://127.0.0.1:8000/company/verified_user"
        let user_data =  {params : {'email': this.email}}
        let res = await this.$axios.get(url, user_data)
        this.users = res.data.list
        console.log(res.data)

        if(res.data.result == true){
          this.user_yes = true
          this.user_no = false
        }
        else{
          this.user_no = true
          this.user_yes = false
        }
       

      },

      async view(email){
        this.$storage.setUniversal('search_email', email)
        this.$router.push('/User_companyprofile')
      },
      async upload(){
        this.company_mail = await this.$storage.getUniversal('hrmail')
        console.log(this.company_mail)
        let formdata= new FormData()
            formdata.append('company_mail',this.company_mail)
            formdata.append('file',this.file)
            let furl = "http://127.0.0.1:8000/hr/uploadcsv"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
      }
    }
  }

</script>

<style>
.personalform {
  width: 100%;
  max-width: 600px; /* Adjust max-width as needed */
  margin: 0 auto;
  padding: 20px;
}
</style>