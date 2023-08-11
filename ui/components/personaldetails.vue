<template>


        <v-container style="width: 100%; ">
          <v-card>
            <v-card-title>Personal Details</v-card-title>
            <v-card-content>
              <v-container>
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
                      <v-icon size="150px" color="yellow" ></v-icon>
                    </v-container>
                    <v-container v-if="verified" class="text-center">
                      <v-icon size="150px" color="green">mdi-check-decagram</v-icon>
                    </v-container>
                    <v-container v-if="rejected" class="text-center">
                      <v-icon size="150px" color="red">mdi-cancel</v-icon>
                    </v-container>
                  </v-col>
                </v-row>
              </v-container>
              <v-row v-if=" !isLoading">
                <v-container >
                  &emsp;&emsp;

                  <v-btn size="30%" v-on:click="verified = true"  :loading="isLoading" :disabled="isLoading" v-if="this.pdata.status == !'verified' || this.pdata.status==!'rejected' " text outlined color="blue ligten-1" style="color:white;" @click="approve(pdata.email, ndata.name)">Approve</v-btn>&emsp;

                  <v-btn size="30%"   :loading="isLoading" :disabled="isLoading" v-if="this.pdata.status == !'verified' || this.pdata.status==!'rejected'" text outlined color="blue lighten-1" style="color:white;"  @click="showForm = true">Reject</v-btn>
                  <v-dialog v-model="showForm" max-width="500px">
                    <v-card>
                      <v-card-title>
                        <span class="headline">Reason</span>
                      </v-card-title>
              
                      <v-card-text>
                        <v-form ref="form" v-model="valid">
                        <v-row>
                          <v-text-field v-model="email_body" label="Enter the Reason for rejection" outlined ></v-text-field>
        
                        </v-row>
                        </v-form>
                      </v-card-text>
              
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="error" text @click="showForm = false">Cancel</v-btn>
                        <v-btn text color="blue lighten-1" :disabled="!valid" @click="deny(pdata.email, ndata.name)"  class="button">Submit</v-btn>
                      </v-card-actions>
            
                    </v-card>
                  </v-dialog>

                </v-container>
              </v-row>


            </v-card-content>

          </v-card>


        </v-container>
</template>

<script>
export default{
    name: 'userprofile',
    async mounted (){
        this.$vuetify.theme.dark =false;
        this.email = this.$storage.getUniversal('user_email')
        let url = "http://127.0.0.1:8000/personal"
        let res = await this.$axios.get(url,{params:{ email :this.email}});
        this.pdata=res.data

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

        this.notary = this.$storage.getUniversal('notaryemail')
        let nurl = "http://127.0.0.1:8000/notary"
        let nres = await this.$axios.get(nurl,{params:{email: this.notary}})
        this.ndata = nres.data
        console.log(this.pdata)

    },
    data: () =>({
        email:"",
        pdata :{},
        ndata:{},
        error: false,
        success: false,
        pending: false,
        verified: false,
        rejected: false,
        isLoading:false,
        email_body:"",
        showForm: false,


    }),
    methods:{
      async approve(email, name){
        let nurl = "http://127.0.0.1:8000/personal/inprogress"
        let ndata={
          'email': this.email,
        }
        let nres = await this.$axios.post(nurl,ndata)

        
       
        
        let url = "http://127.0.0.1:8000/verify/personaldetails"
        let verify={
          user_email: email,
          notary_email: this.ndata.email,
          notary_name: name
        }
        let res = this.$axios.post(url,verify)
        this.isLoading = true;


      },
      async deny(email, name){
        console.log(email, name)
        let url = "http://127.0.0.1:8000/verify/personaldetails"
        let reject={
          user_email: email,
          notary_email: this.ndata.email,
          notary_name: name,
          status: "rejected"
        }
        let res = this.$axios.post(url,reject)
        this.isLoading = true;

        let rurl = "http://127.0.0.1:8000/send_rejection_email"
        let rdata={
          email: email,
          email_subject: "Rejection Mail",
          email_body: `
          Dear Applicant,

          We regret to inform you that your application with Personal Data has been rejected due to ${this.email_body}. Our team reviewed your application carefully, and unfortunately, we are unable to proceed with your application at this time.

          We appreciate your interest in our services and your effort in applying. Thank you for considering us, and reupload the Personal Data .

          With Regards,

          VerifiEdge
        `
        }
        let nres = await this.$axios.post(rurl, rdata)
        this.showForm = false
        this.rejected = true

    }
  }
}
</script>
