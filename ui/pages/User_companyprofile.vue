<template>
    <v-app >
      <v-main class="grey lighten-3">
        <v-container v-if="isAuthenticated">
          <v-row>
            <v-col cols="12" md="3">
  
                <v-container fluid>
                  <v-card class="curved-box" elevation="12">
                    <br><br>
                    <v-row justify="center">
                      <v-col align-self="start" class="d-flex justify-center align-center pa-0" cols="12">
                        <v-avatar class="profile avatar-center-heigth avatar-shadow" color="white" size="170">
                          <input ref="uploader" class="d-none" type="file" accept="image/*" :change="onFileChanged">
                          <v-img src="https://cdn-icons-png.flaticon.com/512/6915/6915987.png"></v-img>
                        </v-avatar>
  
                      </v-col>
                      
                    </v-row>
                    <v-row>
                      <Cuserbanner/>
                    </v-row>
                  </v-card>
                </v-container>
            </v-col>
                
            <v-col cols="12" md="6">
        <Cpersonal/>
  
        <Csslcview/>
  
        <Chseview/>
  
        <Cugview/>
  
        <Cpgview/>
  
        <Cexpview/>
  
            </v-col>
            <v-col >
  
              <v-container fluid>
                <v-card max-width="350px" height="365px" class="mx-auto bg" elevation="2">
                  <br>
                  <v-row justify="center">
                    <v-card-title>Personal Details </v-card-title>
                  </v-row>
                  <br>
                  <v-container>
                    <Cpersonaprofile/>

                  </v-container>

  
                </v-card>
              </v-container>
              <v-container class="text-center">
                <v-btn text outlined @click="back()" color="indigo darken-4">Go Back</v-btn>
              </v-container>
    
  
          </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
    export default {
      layout:'hr_layout',
      

      async mounted(){

        const accessToken = localStorage.getItem('access_token');
        this.isAuthenticated = !!accessToken;
        
        this.email = this.$storage.getUniversal('login_mail')
        let url = "http://127.0.0.1:8000/user"
        let res = await this.$axios.get(url,{params:{email: this.email}})
        this.data= res.data
        console.log(this.data)
        if(this.data.submit_button == false){
          this.show = false
        }
        else{
          this.show = true
        }
  
  
      },
      data: () => ({
        data:{},
        success: false,
        fail: false,
        show: false,
        isAuthenticated: false
        
      }),
      methods:{
        async submit(email){
          console.log(email)
          let nurl = "http://127.0.0.1:8000/user/submit"
          let ndata={
            email: email,
          }
          let nres = await this.$axios.post(nurl,ndata)
          this.pdata = nres.data
          if(this.pdata == true){
            this.success = true
            this.fail = false
          }
          else{
            this.success = false
            this.fail = true
          }
  
  
        },
        async back(){
          this.$router.push('/hrpage')
        }
      }
  
    }
  </script>
  