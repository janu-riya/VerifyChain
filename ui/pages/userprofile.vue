<template>
    <v-main class="grey lighten-3">
      <v-container v-if="isAuthenticated">
        <v-card>
          <v-card-title class="text-h5">XDC Connection</v-card-title>
          <v-card-text>
            <div v-if="!isConnected">
              <p v-if="isMetaMaskInstalled">
                To continue, please connect with XDC:
              </p>
              <p v-else>
                Please install XDC to use this application.
              </p>
              <v-btn @click="get()" color="primary">
                Connect with XDC
              </v-btn>
            </div>
            <div v-else>
              <p>Connected with XDC</p>
              <p>Account: {{ accounts }}</p>
            </div>
          </v-card-text>
        </v-card>
        <v-row>
          <v-col cols="12" md="3">
              <v-container fluid>
                <v-card class="curved-box" elevation="2">
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
                    <userbanner/>
                    <personprofile/>
                    <AddressPage/>
                  </v-row>
                </v-card>
              </v-container>         
          </v-col>
          <v-col cols="12" md="6">
      <personaldetails/>
      <sslcview :contract="contract"/>
      <hseview :contract="contract"/>
      <ugview :contract="contract"/>
      <pgview :contract="contract"/>
      <expview :contract="contract"/>
          </v-col>
          <v-col>

            <v-container fluid>
              <v-card max-width="350px" height="420px" class="mx-auto bg" elevation="2">
                <br>
                <v-row justify="center">
                  <v-card-title></v-card-title>
                </v-row>
                <v-container>
                      <v-container>
                        <v-list>
                          <v-list-item>
                            <v-list-item-title>Verification time</v-list-item-title>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-subtitle>
                              {{ pdata.notary_last_visited }}
                            </v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-title>Last visiting time</v-list-item-title>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-subtitle>
                              {{ pdata.notary_last_visited }}
                            </v-list-item-subtitle>
                          </v-list-item>
                        </v-list>
                      </v-container>
                </v-container>
              </v-card>
            </v-container>
        </v-col>
        </v-row>
      </v-container>
    </v-main>
</template>
<script>
import { ethers } from 'ethers';
import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json"
const contractAddress = '0x51094cD8d5CA57c751328CFDC8b2791D42DB3663'; 
import Web3 from "xdc3"

export default{
    name: 'profile',
    layout:'notary_layout',
    async mounted (){
      const accessToken = localStorage.getItem('access_token');
      this.isAuthenticated = !!accessToken;
        this.$vuetify.theme.dark =false;
        this.email = this.$storage.getUniversal('user_email')
        let url = "http://127.0.0.1:8000/user"
        let res = await this.$axios.get(url,{params:{ email :this.email}});
        this.name=res.data.name

        this.email = this.$storage.getUniversal('user_email')
        let nurl = "http://127.0.0.1:8000/user"
        let nres = await this.$axios.get(nurl,{params:{ email :this.email}});
        this.pdata = nres.data
        console.log(this.pdata)
    },
    data: () =>({
        name : "Sajith Surendran",
        email:"",
        pdata:{},
        connected:false,
        isConnected: false,
        isMetaMaskInstalled: false,
        balance:0,
        input:0,
        accounts: null,
        contract:null,
        isAuthenticated: false
    }),
   methods: {
    async get(){
        if (window.ethereum) {
        window.web3 = new Web3(window.ethereum);
        this.isMetaMaskInstalled = false;
      } else if (window.web3) {
        window.web3 = new Web3(window.web3.currentProvider);
      } else {
        window.alert("Non-Xinfin browser detected. You should consider trying XDCpay");
      }
      this.isMetaMaskInstalled = true;
      this.isConnected = true;
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();
      this.contract = new ethers.Contract(contractAddress, abi.abi, signer);
      
      const web3 = window.web3;
      const accounts = await web3.eth.getAccounts();
      this.accounts = accounts;
      console.log("account",accounts , contractAddress, abi.abi, signer)
    }
   }
}
</script>
