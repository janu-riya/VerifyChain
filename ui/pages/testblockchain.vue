<template>
    <v-app>
      <v-container>
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
                Connect with MetaMask
              </v-btn>
            </div>
            <div v-else>
              <p>Connected with XDC</p>
              <p>Account: {{ accounts }}</p>
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </v-app>
  </template>
  
  <script>
   import { ethers } from 'ethers';
   import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json"
   const contractAddress = '0x51094cD8d5CA57c751328CFDC8b2791D42DB3663'; // Replace with your contract address
// //   const contractABI = abi;
  
//   export default {
//     data() {
//       return {
//         isConnected: false,
//         isMetaMaskInstalled: false,
//         account: null,
//         networkchainID: null,
//         contract: null,
//       };
//     },
//     methods: {
//       async connectWithMetaMask() {
//         if (typeof window.ethereum === 'undefined') {
//           this.isMetaMaskInstalled = false;
//           return;
//         }
  
//         this.isMetaMaskInstalled = true;
  
//         try {
//           await window.ethereum.request({ method: 'eth_requestAccounts' });
//           const provider = new ethers.providers.Web3Provider(window.ethereum);
//           const signer = provider.getSigner();
//           const account = await signer.getAddress();
//           const network = await provider.getNetwork();
  
//           this.isConnected = true;
//           this.account = account;
//           this.networkchainID = network.chainId;
  
//           // Initialize the contract
//           this.contract = new ethers.Contract(contractAddress, abi.abi, signer);
//           console.log(this.contract)
//         } catch (error) {
//           console.error('Error connecting with MetaMask:', error);
//           console.log( contractAddress)
//           console.log(this.contract)

//         }
//       },
  
  
//       async approveFile() {
//     try {
//       if (!this.contract) {
//         console.error('Contract not initialized yet. Please connect with MetaMask first.');
//         return;
//       }

//       const regNo = '12345'; // Replace with the registration number
//       const fileHash = 'kjnkjnkknjk'; // Replace with the file hash
//       const userEmail = "sadasdas@gmail.com"

//       // Call the storeFile function in the contract
//       await this.contract.storeFile(regNo, userEmail, fileHash);

//       console.log('File stored successfully!');
//     } catch (error) {
//       console.error('Error storing file:', error);
//     }
//   },
//     },
//   };

import Web3 from "xdc3"
export default {
  name: 'IndexPage',
  // the connection to wallet is checked using when mounted
  async mounted () {
    // if (window.ethereum) {
    //     window.web3 = new Web3(window.ethereum);
    //     this.connected = true;
    //   } else if (window.web3) {
    //     window.web3 = new Web3(window.web3.currentProvider);
    //   } else {
    //     window.alert("Non-Xinfin browser detected. You should consider trying XDCpay");
    //   }
    //   const web3 = window.web3;
    //   const accounts = await web3.eth.getAccounts();
    //   let accountBalance = await web3.eth.getBalance(accounts[0])
    //   console.log("accountBalance", accountBalance)
    //   console.log("account",accounts)

 

  },
  data: () => ({
    connected:false,
    isConnected: false,
    isMetaMaskInstalled: false,
    balance:0,
    input:0,
    accounts: null,
    contract:null
  }),
  methods:{
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
      console.log(this.contract)
      const web3 = window.web3;
      const accounts = await web3.eth.getAccounts();

      this.accounts = accounts;

      
      console.log("account",accounts)



    },
    // async push(){
        
    //   let contractAddress = "xdc4E09655eA0C15f2c40F22816d59E1a9Bf529627d"
    //   var abi = require('./abi.json');
    //   let contract = new web3.eth.Contract(abi, contractAddress)
    //   // the store method defined in the smart contract Storage.sol is called and the integer value is passed to the funtion also the wallet address of the sender is specified
    //   let result = await contract.methods.store(this.input).send({from:'xdc4a0ff01c148baac9f0e944439627b175d1c5280b'});
    //   console.log(result);
    // }
    async approveFile(){
        try {
      if (!this.contract) {
        console.error('Contract not initialized yet. Please connect with MetaMask first.');
        return;
      }

      const regNo = '12345'; // Replace with the registration number
      const fileHash = 'kjnkjnkknjk'; // Replace with the file hash
      const userEmail = "sadasdas@gmail.com"

      // Call the storeFile function in the contract
      await this.contract.storeFile(regNo, userEmail, fileHash);

      console.log('File stored successfully!');
    } catch (error) {
      console.error('Error storing file:', error);
    }
    }
  }
}


  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  

   <!-- <template>
    <v-app>
      <v-container>
        <v-card>
          <v-card-title class="text-h5">XDCpay Wallet Connection</v-card-title>
          <v-card-text>
            <div v-if="!isConnected">
              <p v-if="isXDCpayInstalled">
                To continue, please connect with XDCpay Wallet:
              </p>
              <p v-else>
                Please install XDCpay Wallet to use this application.
              </p>
              <v-btn @click="connectWithXDCpay" color="primary">
                Connect with XDCpay Wallet
              </v-btn>
            </div>
            <div v-else>
              <p>Connected with XDCpay Wallet</p>
              <p>Account: {{ account }}</p>
              <p>ChainID: {{ networkchainID }}</p>
              <v-btn @click="approveFile" color="primary">Approve</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </v-app>
  </template>
  
  <script>
  import { Xdc3 } from "xdc3";
  import abi from "../app/src/artifacts/contracts/FIlestorage.sol/FileStorage.json";
  
  const contractAddress = "0x574F493E8FfDA4Df12cD6b99c3DA506b00102F89"; // Replace with your contract address
  const contractABI = abi;
  
  export default {
    data() {
      return {
        isConnected: false,
        isXDCpayInstalled: false,
        account: null,
        networkchainID: null,
        contract: null,
      };
    },
    methods: {
      async connectWithXDCpay() {
        // if (typeof window.xdc3 === "undefined") {
        //   this.isXDCpayInstalled = false;
        //   return;
        // }
  
        this.isXDCpayInstalled = true;
  
        try {
            const provider = new Xdc3(window.xdc3.givenProvider); // Replace 'window.xdc3' with the actual XDCpay Wallet object
          const accounts = await provider.request({
            method: "eth_requestAccounts",
          });
          const account = accounts[0];
          const network = await provider.request({ method: "eth_chainId" });
  
          this.isConnected = true;
          this.account = account;
          this.networkchainID = network;
  
          // Initialize the contract
          this.contract = new provider.Contract(
            contractABI,
            contractAddress
          ).connect(account);
          console.log(this.account);
        } catch (error) {
          console.error("Error connecting with XDCpay Wallet:", error);
        }
      },
  
      async approveFile() {
        try {
          if (!this.contract) {
            console.error(
              "Contract not initialized yet. Please connect with XDCpay Wallet first."
            );
            return;
          }
  
          const regNo = "12345"; // Replace with the registration number
          const fileHash = "YOUR_FILE_HASH"; // Replace with the file hash
          const userEmail = "sadasdas@gmail.com";
  
          // Call the storeFile function in the contract
          await this.contract.storeFile(regNo, userEmail, fileHash);
  
          console.log("File stored successfully!");
        } catch (error) {
          console.error("Error storing file:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
   -->