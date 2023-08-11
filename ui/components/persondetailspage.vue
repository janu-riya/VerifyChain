<template>
  <v-container style="width: 100%; ">
    <v-card class="curved-box" elevation="12">
      <v-container v-if="data_">
        <div class="custom-alert">
            <v-icon class="alert-icon">mdi-alert-circle</v-icon>
            <span>Personal Data is mandatory.</span>
          </div>
      </v-container>
      <v-card-title>Personal Details</v-card-title>
      <v-card-content>
        <v-container v-if="data_s">
          <v-row>
            <v-col style="padding-left: 4%;">
              <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc;">
                
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Mobile Number:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ pdata.mob }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">PAN Number:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ pdata.pan }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Company Name :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ pdata.company_name }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Designation :</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ pdata.designation }}</h5></td>
                </tr>
              </table>
              <br>
              <h6 class="text-subtitle-3"> Submitted on : {{ pdata.submitted_on }}</h6>
              <h6 v-if="pdata.edited_on" class="text-subtitle-3"> Edited on : {{ pdata.edited_on }}</h6>
              <h6 v-if="pdata.approved_on, verified" class="text-subtitle-3"> Approved on : {{ pdata.approved_on }}</h6>

            </v-col>
            <v-col >
              <v-container v-if="pending" class="text-center">
              </v-container>
              <v-container v-if="pdata.status == 'verified'" class="text-center">
                <v-icon size="150px" color="green">mdi-check-decagram</v-icon>
              </v-container>
              <v-container v-if="pdata.status == 'rejected'" class="text-center">
                <v-icon size="150px" color="red">mdi-cancel</v-icon>
                <br>
                <v-btn color="blue lighten-1" style="color: white;" @click="edit()">EDIT</v-btn>
              </v-container>

            </v-col>


          </v-row>
        </v-container>
      </v-card-content>
      <v-card-action >
        <v-container v-if="data_">
          <v-btn text icon @click="addpersonal()"><v-icon color="blue lighten-1">mdi-plus</v-icon></v-btn>

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
  let url = "http://127.0.0.1:8000/personal"
  let res = await this.$axios.get(url,{params:{ email :this.email}});
  this.pdata=res.data
  console.log(this.pdata)

  if(this.pdata == false){
        this.data_ = true,
        this.data_s = false
      }
      else{
        this.data_s = true,
        this.data_ = false
      }
  if (this.pdata.status == "pending"){
          this.pending = true
          this.verified = false
          this.rejected = false
        }
        if(this.pdata.status == "verified"){
          this.verified = true
          this.pending = false
          this.rejected = false
        }
        if(this.pdata.status == "rejected"){
          this.rejected = true
          this.pending = false
          this.verified = false
        }


},
data: () =>({
  email:"",
  pdata :{},
  pending: false,
  verified: false,
  rejected: false,
  data_: false,
  data_s: false
}),
methods:{
  async edit(){
    this.$router.push("/personal_edit")
  },
  async addpersonal(){
    this.$router.push('/onboard')
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