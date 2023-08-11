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
          <h6 v-if="data.approved_on, verified" class="text-subtitle-3"> Approved on : {{ data.approved_on }}</h6>


            </v-col>
            <v-col>
              <v-container v-if="pending" class="text-center">
                <v-icon size="150px" color="yellow" ></v-icon>
              </v-container>
              <v-container v-if="data.status == 'verified'" class="text-center">
                <v-icon size="150px" color="green">mdi-check-decagram</v-icon>

              </v-container>
              <v-container v-if="data.status == 'rejected'" class="text-center">
                <v-icon size="150px" color="red">mdi-cancel</v-icon>

              </v-container>
              <br>
            </v-col>
          </v-row>
        </v-container>
        <v-row>
          <v-container>
  
            &emsp;&emsp;
            <v-btn text outlined color="blue lighten-1"  @click="doc(data.email, data.empid)">Document</v-btn>
            <br><br>
            <v-divider thickness="2" color="blue lighten-1"></v-divider>
          </v-container>
  
        </v-row>
      </v-card-content>
      
    </v-card>

      </v-container>
</template>
<script>
import { ethers } from 'ethers';
import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json"
const contractAddress = '0x51094cD8d5CA57c751328CFDC8b2791D42DB3663'; 
import Web3 from "xdc3"
export default{
  name: 'hse',
  async mounted (){
      this.$vuetify.theme.dark =false;
      this.email = this.$storage.getUniversal('search_email')
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
      if (this.datas.status == false){
          this.pending = true
          this.verified = false
          this.rejected = false
        }
        if(this.datas.status == "verified"){
          this.verified = true
          this.pending = false
          this.rejected = false
        }
        if(this.datas.status == "rejected"){
          this.rejected = true
          this.pending = false
          this.verified = false
        }
  },
  data: () =>({
      email:"",
      datas:[],
      pending: false,
      verified: false,
      rejected: false,
      data_: false,
      data_s: false,
      contract: null



  }),
  methods:{
    async doc(email, empid){
      let hurl = "http://127.0.0.1:8000/Hash/S3files"
      let hres = await this.$axios.get(hurl,{params:{email: email, regno: empid}})
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

      const regNo = empid // Replace with the registration number
      const userEmail = this.email

      // Call the storeFile function in the contract
      this.get = await this.contract.getFile(regNo, userEmail);
      this.blockhash = this.get[2]
      console.log(this.blockhash);
    } catch (error) {
      console.error('Error getting file:', error);
    }

    if(this.blockhash == this.hash){
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
    }
    else{
      console.log('error')
    }

    },
   }
}
</script>
