<template>
    <v-container style="width: 100%; ">
      <v-card>
        <v-card-title>HSE Details</v-card-title>
        <v-card-content>
          <v-container>
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
              <h6 v-if="data.approved_on, verified" class="text-subtitle-3"> Approved on : {{ data.approved_on }}</h6>

              </v-col>
              <v-col >
                <v-container v-if="pending" class="text-center">
                  <v-icon size="150px" color="yellow" ></v-icon>
                </v-container>
                <v-container v-if="verified " class="text-center">
                  <v-icon size="150px" color="green">mdi-check-decagram</v-icon>
                </v-container>
                <v-container v-if="rejected" class="text-center">
                  <v-icon size="150px" color="red">mdi-cancel</v-icon>
                </v-container>
                <br>
              </v-col>
            </v-row>
          </v-container>
          <v-row>
            <v-container  v-if="!isLoading">
              &emsp;&emsp;
              <v-btn size="30%"   :loading="isLoading" :disabled="isLoading" v-if="this.data.status == !'verified' || this.data.status==!'rejected'" text outlined  color="blue lighten-1" style="color:white;" @click="approve(data.email, data.hse_regno, ndata.name)">Approve</v-btn>&emsp;
              <v-btn size="30%"   :loading="isLoading" :disabled="isLoading" v-if="this.data.status == !'verified' || this.data.status==!'rejected'" text outlined  color="blue lighten-1" style="color:white;" @click="showForm = true">Reject</v-btn>&emsp;
            </v-container>
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
                  <v-btn text color="blue lighten-1" :disabled="!valid" @click="deny(data.email, data.hse_regno, ndata.name)" class="button">Submit</v-btn>
                </v-card-actions>
      
              </v-card>
            </v-dialog>
          </v-row>
          <v-row>
            <v-container>
              &emsp;&emsp;
  
              <v-btn size="30%" text outlined  color="blue lighten-1" style="color: white;" @click="doc(data.email, data.hse_regno)">Document</v-btn>
  
            </v-container>
          </v-row>
          <v-container v-if="fail" class="text-center">
          <v-alert   type="error" dismissible> Check Whether you have connected your wallet </v-alert>
          </v-container>
        </v-card-content>
        

      </v-card>
        </v-container>
</template>
<script>
import { ethers } from 'ethers';
import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json"
export default{
    name: 'hse',
    props: {
    contract: {
      type: Object,
      required: true,
    },
  },
    async mounted (){
        this.$vuetify.theme.dark =false;
        this.email = this.$storage.getUniversal('user_email')
        let url = "http://127.0.0.1:8000/hse"
        let res = await this.$axios.get(url,{params:{email: this.email}})
        this.data= res.data

        this.notary = this.$storage.getUniversal('notaryemail')
        let nurl = "http://127.0.0.1:8000/notary"
        let nres = await this.$axios.get(nurl,{params:{email: this.notary}})
        this.ndata = nres.data
        console.log(this.contract)


        if (this.data.status == false){
          this.pending = true
          this.verified = false
          this.rejected = false
        }
        if(this.data.status == "verified"){
          this.verified = true
          this.pending = false
          this.rejected = false
        }
        if(this.data.status == "rejected"){
          this.rejected = true
          this.pending = false
          this.verified = false
        }


    },
    data: () =>({
        email:"",
        data:{},
        ndata: {},
        pending: false,
        verified: false,
        rejected: false,
        isLoading:false,
        pushed: false,
        email_body:"",
        showForm: false,
        fail: false

    }),
    methods:{
    async doc(email, hse_regno){
      this.$axios.get("http://127.0.0.1:8000/download/S3files",{
        params:{
          email: email,
          regno: hse_regno
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
    async approve(email, hse_regno, name){
      this.fail = false

      let nurl="http://127.0.0.1:8000/hse/inprogress"
      let ndata={
        'email':this.email,
      }
      let nres=await this.$axios.post(nurl,ndata)

      //Hash conversion

      let hurl = "http://127.0.0.1:8000/Hash/S3files"
      let hres = await this.$axios.get(hurl,{params:{email: this.email, regno: hse_regno}})
      this.hash = hres.data
      console.log(this.hash)
      
      // Blockchain Code
      try {
      if (!this.contract) {
        console.error('Contract not initialized yet. Please connect with MetaMask first.');
        this.fail = true
        return;
      }
     
      const regNo = hse_regno // Replace with the registration number
      const fileHash = this.hash// Replace with the file hash
      const userEmail = this.email

      // Call the storeFile function in the contract
      await this.contract.storeFile(regNo, userEmail, fileHash);

      const status = 'File stored successfully!'
      console.log('File stored successfully!');
      
      this.render = false;
      if (status == 'File stored successfully!'){
      let url= "http://127.0.0.1:8000/verify/hse"
      let verify = {
        user_email: email,
        hse_regno: hse_regno,
        notary_email: this.ndata.email,
        notary_name: name
      }
      let res = this.$axios.post(url, verify)
      this.isLoading = true;
    }
    } catch (error) {
      console.error('Error storing file:', error);
    }
      this.verified = true;




    },
    async deny(email, hse_regno, name){
        console.log(email, name)
        let url = "http://127.0.0.1:8000/verify/hse"
        let reject={
          user_email: email,
          hse_regno: hse_regno,
          notary_email: this.ndata.email,
          notary_name: name,
          status: "rejected"
        }
        let res = this.$axios.post(url,reject)
        this.isLoading = true;

        let rurl = "http://127.0.0.1:8000/send_rejection_email"
        let rdata={
          email: email,
          email_subject: "HSE Rejection",
          email_body: `
            Dear Applicant,

            We regret to inform you that your application with HSE Data   has been rejected due to ${this.email_body}. Our team reviewed your application carefully, and unfortunately, we are unable to proceed with your application at this time.

            We appreciate your interest in our services and your effort in applying. Thank you for considering us, and reupload the HSE Data .

            With Regards,

            VerifiEdge

        `
        }
        let nres = await this.$axios.post(rurl, rdata)
        console.log(nres)
        this.showForm = false
        this.rejected = true

    }
   }
}
</script>
