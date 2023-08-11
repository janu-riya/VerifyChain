<template>
  <v-container style="width: 100%; " v-if="data_s">
    <v-card>
      <v-card-title>Exp Details</v-card-title>
      <v-card-content v-for="data in datas" :key="data.email">
        <v-container >
          <v-row>
            <v-col style="padding-left: 4%; ">
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
            <v-col>
              <v-container v-if="pending" class="text-center">
                <v-icon size="150px" color="yellow" ></v-icon>
              </v-container>
              <v-container v-if="data.status  == 'verified' && !isLoading" class="text-center">
                <v-icon size="150px" color="green">mdi-check-decagram</v-icon>

              </v-container>
              <v-container v-if="data.status == 'rejected' " class="text-center">
                <v-icon size="150px" color="red">mdi-cancel</v-icon>

              </v-container>

            </v-col>
          </v-row>
          
        </v-container>
        <v-row>
          <v-container>
            &emsp;&emsp;
            <v-btn size="30%"  :loading="isLoading" :disabled="isLoading" v-if="data.status == !'verified' || data.status==!'rejected'" text outlined color="blue lighten-1" style="color: white;"  @click="approve(data.email, data.empid, ndata.name)">Approve</v-btn>&emsp;
            <v-btn size="30%"   :loading="isrejecting" :disabled="isrejecting" v-if="data.status == !'verified' || data.status==!'rejected'" text outlined  color="blue lighten-1" style="color: white;"   @click="openRejectDialog(data.email, data.empid, ndata.name)">Reject</v-btn>
            <v-dialog  v-model="showForm" max-width="500px">
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
                  <v-btn text color="blue lighten-1" :disabled="!valid"   @click="deny(rejectionData.email, rejectionData.empid, rejectionData.name, email_body)">Submit</v-btn>
                </v-card-actions>
      
              </v-card>
            </v-dialog>
          </v-container>
        </v-row>
        <v-row>
          <v-container>
            &emsp;&emsp;

            <v-btn size="30%" text outlined  color="blue lighten-1" style="color: white;" @click="doc(data.email, data.empid)">Document</v-btn>

          </v-container>
        </v-row>
      </v-card-content>
      <v-container v-if="fail" class="text-center">
        <v-alert   type="error" dismissible> Check Whether you have connected your wallet </v-alert>
        </v-container>
    </v-card>
  </v-container>
</template>
<script>
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
      let url = "http://127.0.0.1:8000/exp"
      console.log(this.email)
      let res = await this.$axios.get(url,{params:{email: this.email}})
      this.datas= res.data
      console.log(this.datas)

      if(this.datas == false){
        this.data_ = true,
        this.data_s = false
      }
      else{
        this.data_s = true,
        this.data_ = false
      }

      this.notary = this.$storage.getUniversal('notaryemail')
        let nurl = "http://127.0.0.1:8000/notary"
        let nres = await this.$axios.get(nurl,{params:{email: this.notary}})
        this.ndata = nres.data


      console.log(this.datas)

  },
  data: () =>({
      email:"",
      datas:[],
      pending: false,
      verified: false,
      rejected: false,
      data_: false,
      data_s: false,
      isLoading:false,
      isrejecting: false,
      email_body:"",
      showForm: false,
      fail: false,
      rejectionData: {
    email: '',
    empid: '',
    name: '',
  },



  }),
  methods:{
    openRejectDialog(email, empid, name) {
    this.rejectionData.email = email;
    this.rejectionData.empid = empid;
    this.rejectionData.name = name;
    this.showForm = true;
  },
   
    async approve(email, empid, name){
      this.fail = false

      let nurl = "http://127.0.0.1:8000/exp/inprogress"
      let data={
        'email':this.email,
      }
      let nres= await this.$axios.post(nurl,data)
      console.log(this.datas.status)
      
      //Hash conversion

      let hurl = "http://127.0.0.1:8000/Hash/S3files"
      let hres = await this.$axios.get(hurl,{params:{email: email, regno: empid}})
      this.hash = hres.data
      console.log(this.hash)

      // Blockchain Code
      try {
      if (!this.contract) {
        console.error('Contract not initialized yet. Please connect with MetaMask first.');
        this.fail = true
        return;
      }
     
      const regNo = empid // Replace with the registration number
      const fileHash = this.hash// Replace with the file hash
      const userEmail = this.email

      // Call the storeFile function in the contract
      await this.contract.storeFile(regNo, userEmail, fileHash);

      const status = 'File stored successfully!'
      console.log('File stored successfully!');
      
      this.render = false;
      if (status == 'File stored successfully!'){
        let url = "http://127.0.0.1:8000/verify/exp"
        let verify={
        user_email: email,
        empid: empid,
        notary_email: this.ndata.email,
        notary_name: name
      }
      let res = await this.$axios.post(url, verify)
      window.location.reload()
      }
    } catch (error) {
      console.error('Error storing file:', error);
    }

      
      


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
    async deny(email, empid, name){
      console.log(email, empid)
      let url = "http://127.0.0.1:8000/verify/exp"
        let reject={
          user_email: email,
          empid: empid,
          notary_email: this.ndata.email,
          notary_name: name,
          status: "rejected"
        }
        let res = this.$axios.post(url,reject)
        let rurl = "http://127.0.0.1:8000/send_rejection_email"
        let rdata={
          email: email,
          email_subject: "EXperience data Rejection",
          email_body: `
          Dear Applicant,

          We regret to inform you that your application with Experience Data has been rejected due to ${this.email_body}. Our team reviewed your application carefully, and unfortunately, we are unable to proceed with your application at this time.

          We appreciate your interest in our services and your effort in applying. Thank you for considering us, and reupload the Expereince Data .

          With Regards,

          VerifiEdge

          `
        }
        let nres = await this.$axios.post(rurl, rdata)
        console.log(nres)
        this.showForm = false
        this.isrejecting = true
        window.location.reload()

    }
   }
}
</script>
