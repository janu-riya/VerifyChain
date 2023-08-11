<template>
  <v-container style="width: 100%; ">
    <v-card class="curved-box" elevation="12">
      <v-container v-if="data_">
        <div class="custom-alert">
            <v-icon class="alert-icon">mdi-alert-circle</v-icon>
            <span>HSE Data is mandatory.</span>
          </div>
      </v-container>
      <v-card-title>HSE Details</v-card-title>
      <v-card-content>
        <v-container v-if="data_s">
          <v-row>
            <v-col style="padding-left: 4%;">
              <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc;">
                
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Register Number:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.hse_regno }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Marks:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.hse_marks }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">School:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.hse_school }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Board:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.hse_board }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Year of Completion:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.hse_passout }}</h5></td>
                </tr>
                
              </table>
              <br>
              
          <h6 class="text-subtitle-3"> Submitted on : {{ data.submitted_on }}</h6>
              <h6 v-if="data.edited_on" class="text-subtitle-3"> Edited on : {{ data.edited_on }}</h6>
              <h6 v-if="data.approved_on, data.status == 'verified'" class="text-subtitle-3"> Approved on : {{ data.approved_on }}</h6>

            </v-col>
            <v-col >
              <v-container v-if="pending" class="text-center">
                <v-icon size="150px" color="yellow" ></v-icon>
              </v-container>
              <v-container v-if="data.status == 'verified'" class="text-center">
                <v-icon size="150px" color="green">mdi-check-decagram</v-icon>
              </v-container>
              <v-container v-if="data.status == 'rejected'" class="text-center">
                <v-icon size="150px" color="red">mdi-cancel</v-icon>
                <br>
                <v-btn color="blue lighten-1" style="color: white;" @click="edit()">EDIT</v-btn>
              </v-container>

              


            </v-col>


          </v-row>
          <v-row>
            <v-container  v-if="this.datapdf == true || show">
              &emsp;&emsp;
  
              <v-btn size="30%" text outlined color="blue lighten-1" style="color: white;" @click="doc(data.email, data.hse_hse_regno)">Document</v-btn>
  
            </v-container>
          </v-row>
          <v-row>
            <v-col v-if="this.datapdf == false  &&!isLoading">
           
                <v-file-input  style="width:60%;" @change="fileselect"  label = "Upload HSE doc" ></v-file-input>
      
            </v-col>
            <v-col>
              <v-container v-if="this.datapdf == false  &&!isLoading">
                <v-btn size="30%" v-on:click="show = true"  :loading="isLoading" :disabled="isLoading"  text outlined color="blue lighten-1" style="color: white;" @click="upload()">Upload</v-btn>
              </v-container>
            </v-col>
          </v-row>
        </v-container>
        
  
      </v-card-content>
      <v-card-action >
        <v-container v-if="data_">
          <v-btn text icon @click="addhse()"><v-icon color="blue lighten-1">mdi-plus</v-icon></v-btn>

        </v-container>

      </v-card-action>


    </v-card>


      </v-container>
</template>
<script>
export default{
  name: 'hse',
  async mounted (){
      this.$vuetify.theme.dark =false;
      this.email = this.$storage.getUniversal('login_mail')
      let url = "http://127.0.0.1:8000/hse"
      let res = await this.$axios.get(url,{params:{email: this.email}})
      this.data= res.data
      this.regno = res.data.hse_regno

      if(this.data == false){
        this.data_ = true,
        this.show = true,
        this.data_s = false
      }
      else{
        this.data_s = true,
        this.data_ = false
      }

      let nurl = "http://127.0.0.1:8000/check-s3-folder"
      let nres = await this.$axios.get(nurl,{params:{email: this.email, regno: this.regno}})
      this.datapdf = nres.data.file_present
      if(this.datapdf == true){
        this.show = true
      }
  },
  data: () =>({
      email:"",
      regno:"",
      datapdf:"",
      isLoading:false,
      data:{},
      pending: false,
      verified: false,
      rejected: false,
      data_s: false,
      data_: false,
      show: false

  }),
  methods:{
    async fileselect(event){
      this.file=event
    },
    async upload(){
      let nurl = "http://127.0.0.1:8000/user/expupdation"
        let ndata={
          'email': this.email
        }
        let nres = await this.$axios.post(nurl, ndata)

            let formdata= new FormData()
            formdata.append('email',this.email)
            formdata.append('regno',this.regno)
            formdata.append('file',this.file)
            let furl = "http://127.0.0.1:8000/uploadfile/S3"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
            
            this.isLoading = true;
            // Simulate an asynchronous operation, such as an API call
     
   },

    async doc(email, hse_regno){
      this.$axios.get("http://127.0.0.1:8000/download/S3files",{
        params:{
          email: email,
          regno: this.regno
        },
        responseType: 'arraybuffer'
      })
      .then(response => {
        console.log(response)

        let blob = new Blob([response.data], { type: 'application/pdf'}),
        url = window.URL.createObjectURL(blob)

        window.open(url)
      })
      console.log(hse_regno)

    },
    async edit(){
      this.$router.push('/hse_edite')
    },
    async addhse(){
      this.$router.push('/hsepage')
    }
   }
}
</script>
<style>
.curved-box {
    border-radius: 40px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
  }
.custom-alert {
  display: flex;
  align-items: center;
  background-color: transparent;
  color: #008cff; 
}

.custom-alert .alert-icon {
  color: #008cff; 
  margin-right: 5px;
}

.custom-alert .alert-text {
  font-size: 16px;
}

</style>
