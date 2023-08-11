<template>
   <v-container style="width: 100%; ">
    <v-card>
      <v-card-title>SSLC Details</v-card-title>
      <v-card-content>
        <v-container>
          <v-row>
            <v-col style="padding-left: 4%;">
              <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc;">
                
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Register Number:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.sslc_regno }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Marks:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.sslc_marks }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">School:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.sslc_school }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Board:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.sslc_board }}</h5></td>
                </tr>
                <tr style="border-bottom: 1px solid #ccc;">
                  <td style="padding: 10px;"><h4 class="text-subtitle-3">Year of Completion:</h4></td>
                  <td style="padding: 10px;"><h5 class="text-subtitle-3">{{ data.sslc_passout }}</h5></td>
                </tr>
              </table>
              <br>
          <h6 class="text-subtitle-3"> Submitted on : {{ data.submitted_on }}</h6>
          <h6 v-if="data.approved_on, verified" class="text-subtitle-3"> Approved on : {{ data.approved_on }}</h6>

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
      </v-card-content>
      <v-row>
        <v-container>
          &emsp; &emsp;
          <v-btn text outlined color="blue lighten-1" style="color: white;" @click="doc(data.email, data.sslc_regno)">Document</v-btn>

        </v-container>
      </v-row>



    </v-card>




        </v-container>
</template>
<script>
import { ethers } from 'ethers';
import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json"
const contractAddress = '0x51094cD8d5CA57c751328CFDC8b2791D42DB3663'; 
import Web3 from "xdc3"
export default{
    name: 'userprofile',
    async mounted (){
        this.$vuetify.theme.dark =false;
        this.email = this.$storage.getUniversal('search_email');
        let url = "http://127.0.0.1:8000/sslc"
        let res = await this.$axios.get(url,{params:{email: this.email}})
        this.data= res.data
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
        pending: false,
        verified: false,
        rejected: false,
        contract: null
    }),
    methods:{
      async doc(email, sslc_regno){

      let hurl = "http://127.0.0.1:8000/Hash/S3files"
      let hres = await this.$axios.get(hurl,{params:{email: email, regno: sslc_regno}})
      this.hash = hres.data
      console.log(this.hash)

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const web3 = window.web3;
      const signer = provider.getSigner();

      this.contract = new ethers.Contract(contractAddress, abi.abi, signer);
      console.log(this.contract)
      try {
      if (!this.contract) {
        console.error('Contract not initialized yet. Please connect with MetaMask first.');
        return;
      }

      const regNo = sslc_regno // Replace with the registration number
      const userEmail = this.email

      // Call the storeFile function in the contract
      this.get = await this.contract.getFile(regNo, userEmail);
      this.blockhash = this.get[2]
      console.log(this.blockhash);
    } catch (error) {
      console.error('Error getting file:', error);
    }

    if(this.blockhash == this.hash){
      let url = "http://127.0.0.1:8000/download/S3files"

      this.$axios.get(url,{
        params:{
          email: email,
          regno: sslc_regno
        },
        responseType: 'arraybuffer'
      })
      .then(response => {
        console.log(response)
        if(response.data == false){
          this.error == true
        }
        else{
          this.error = false
          let blob = new Blob([response.data], { type: 'application/pdf'}),
        url = window.URL.createObjectURL(blob)

        window.open(url)
        }
      })
      console.log(sslc_regno)
    } 
    else{
      console.log('error')
    }
    },
   }
}
</script>
