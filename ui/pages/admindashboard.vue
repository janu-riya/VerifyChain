<template>
 
      
  <v-container>
    
      <v-col>
        <v-row>
          <v-col>
            <v-card height="150.5px" style="background-color: #BBDEFB;">
              <v-card-title>Total </v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ counts }}</h1></v-card-title>
            </v-card>
          </v-col>
          <v-col>
            <v-card height="150.5px" style="background-color: #90CAF9;">

              <v-card-title >PENDING </v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count }}</h1></v-card-title>
            </v-card>

          </v-col>
          <v-col>
            <v-card height="150.5px" style="background-color: #64B5F6;">

              <v-card-title>INPROGRESS </v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count2 }}</h1></v-card-title>

            </v-card>

          </v-col>
          <v-col>
            <v-card height="150.5px" style="background-color: #42A5F5;">
              <v-card-title>COMPLETED </v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count1 }}</h1></v-card-title>
          </v-card>
          </v-col>

        </v-row>
            <v-container>
            <v-tabs
            v-model="tabs"
            centered
          >
            <v-tab
              v-for="n in 1"
              :key="n"
            >
              pending 
            </v-tab>
            <v-tab
              v-for="n in 1"
              :key="n"
            >
              Inprogress 
            </v-tab>
            <v-tab
              v-for="n in 1"
              :key="n"
            >
              Approved
            </v-tab>
          </v-tabs>
          </v-container>
          </v-col>
          

          <v-container style="margin-bottom: 50%;">
              <v-tabs-items v-model="tabs">
        <v-tab-item>
          <v-card>
            <v-card-text>
                <notaryusers/>

            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card >

            <notaryinprogress/>

          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card>

            <notaryapproved/>

          </v-card>
        </v-tab-item>
      </v-tabs-items>
            
          </v-container>
        </v-container>
          
       
        



  </template>
   


  
  <script >
  export default {
    name :"notary",
  layout: "notary_layout",
    async mounted () {
    this.$vuetify.theme.dark = false
    return {
        tabs: null,
        text:'something happen', 
    }
 
  },

  methods: {
    dashboard() {
      this.$router.push('/dashboard');
    },
    profile() {
      this.$router.push('/profile');
    },
    file() {
      this.$router.push('/file');
    },
    recent() {
      this.$router.push('/resent');
    },
    recovery() {
      this.$router.push('/recovery');
    },
    help() {
      this.$router.push('/help');
    },
    storage() {
      this.$router.push('/storage');
    },
    settings() {
      this.$router.push('/settings');
    },
    logout() {
      this.$router.push('/logout');
    },
  },
name :"notary",
  layout: "notary_layout",
  async mounted(){
    this.$vuetify.theme.dark =false;
    let url = "http://127.0.0.1:8000/pendinguser"
        let res = await this.$axios.get(url)
        this.profiles = res.data.list
        this.count = res.data.count

        let rurl = "http://127.0.0.1:8000/inprogressuser"
    let rres = await this.$axios.get(rurl)
    this.count2 = rres.data.count


    let surl = "http://127.0.0.1:8000/verifiedusers"
    let sres = await this.$axios.get(surl)
    this.count1 = sres.data.count1

    let turl = "http://127.0.0.1:8000/totalprofile"
    let tres = await this.$axios.get(turl)
    this.counts = tres.data.counts

   

    this.$vuetify.theme.dark =false;
    this.email = this.$storage.getUniversal('notaryemail')
    let nurl = "http://127.0.0.1:8000/notary"
    let nres = await this.$axios.get(nurl,{params:{ email :this.email}});
    this.pdata = nres.data
    console.log(this.pdata)

  },
  data: () => ({
      reveal: false,
      reveal2:false,
      approve: false,
      count:{},
      count1:{},
      count2:{},
      counts:{},
      pdata:{},
      drawer: false,
      tabs: null,
    }),
  }
</script>

