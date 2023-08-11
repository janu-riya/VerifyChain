<template>
  <v-container style="width: 100%; ">
    <v-container>
      <v-switch
      v-model="expshow"
      hide-details
      inset
      label="I am Fresher"
      >

      </v-switch>
    </v-container>

    <v-card class="curved-box" elevation="12" v-if="!expshow">
      <v-card-title>Experience Details</v-card-title>
      <v-card-content  v-for="data in datas" :key="data.email">
        <v-container v-if="data_s">
          <v-row>
            <v-col style="padding-left: 4%;">
              <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc;">
                
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Emp ID :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.empid }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Company:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.company_name }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Start Date :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.start_date }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">End Date :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.end_date }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Designation :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.designation }}</h5></td>
                </tr>
              </table>
              <br>
          <h6 class="text-subtitle-3"> Submitted on : {{ data.submitted_on }}</h6>
          <h6 v-if="data.edited_on" class="text-subtitle-3"> Edited on : {{ data.edited_on }}</h6>
          <h6 v-if="data.approved_on" class="text-subtitle-3"> Approved on : {{ data.approved_on }}</h6>
            </v-col>
            <v-col style="margin-top: -5%;">
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
            <v-container v-if="datapdf == true || show">
              &emsp;&emsp;
              <v-btn text outlined color="blue lighten-1" style="color: white;" @click="doc(data.email, data.empid)">Document</v-btn>
            </v-container>
          </v-row>
          <v-row>
            <v-col v-if="datapdf == false">
                <v-file-input  style="width:60%;" @change="fileselect"  label = "Upload Exp doc" ></v-file-input>
            </v-col>
            <v-col>
              <v-container v-if="datapdf == false">
                <v-btn size="30%" v-on:click="show = true"  :loading="isLoading" :disabled="isLoading"  text outlined color="blue lighten-1" style="color: white;" @click="upload(data.email, data.empid)">Upload</v-btn>
              </v-container>
            </v-col>
          </v-row>
        </v-container>
        

        
      </v-card-content>
      <v-card-action >
        <v-container v-if="data_">
          <v-btn text icon @click="addsslc()"><v-icon color="blue lighten-1">mdi-plus</v-icon></v-btn>

        </v-container>
        <v-container v-if="data_s">
          <v-btn text icon @click="addsslc()"><v-icon color="blue lighten-1">mdi-plus</v-icon></v-btn>
        </v-container>

      </v-card-action>


    </v-card>


       </v-container>
</template>
<script>
export default{
   name: 'userprofile',
   async mounted (){
       this.$vuetify.theme.dark =false;
       this.email = this.$storage.getUniversal('login_mail')
       let url = "http://127.0.0.1:8000/exp"
       let res = await this.$axios.get(url,{params:{email: this.email}})
       this.datas= res.data
       
       if(this.datas == false){
        this.data_ = true,
        this.data_s = false
      }
      else{
        this.data_s = true,
        this.value = res.data[0].empid
        this.data_ = false
      }

      let nurl = "http://127.0.0.1:8000/check-s3-folder"
      let nres = await this.$axios.get(nurl,{params:{email: this.email, regno: this.value }})
      this.datapdf = nres.data.file_present
      console.log(this.datapdf)
      if(this.datapdf == true){
        this.show = true
      }
      


   },
   data: () =>({
       email:"",
       regno:"",
       datapdf:"",
       datas:[],
       pending: false,
       verified: false,
       rejected: false,
       data_s: false,
       data_: false,
       expshow: false,
       isLoading: false,
       show: false

   }),
   methods:{

    async fileselect(event){
      this.file=event
    },
    async upload(email, empid){
      let nurl = "http://127.0.0.1:8000/user/expupdation"
        let ndata={
          'email': this.email
        }
        let nres = await this.$axios.post(nurl, ndata)

            let formdata= new FormData()
            formdata.append('email', email)
            formdata.append('regno', empid)
            formdata.append('file',this.file)
            let furl = "http://127.0.0.1:8000/uploadfile/S3"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
            
            this.isLoading = true;
            window.location.reload();
            // Simulate an asynchronous operation, such as an API call
            
   },
    async doc(email, empid){
      console.log(empid)
      this.$axios.get("http://127.0.0.1:8000/download/S3files",{
        params:{
          email: email,
          regno: empid
        },
        
        responseType: 'arraybuffer'
      })
      .then(response => {
        console.log(response)

        let blob = new Blob([response.data], { type: 'application/pdf'}),
        url = window.URL.createObjectURL(blob)

        window.open(url)
      })

    },
    async edit(){
      this.$router.push('/exp_edit')
    },
    async addsslc(){
      this.$router.push('/exppage')
    }
   }
}
</script>
<style>
.curved-box {
    border-radius: 40px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
  }
</style>