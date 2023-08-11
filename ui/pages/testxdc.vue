<template>
    <v-btn @click="get()">Connect with XDC Pay</v-btn>
  </template>
  
  <script>
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
    balance:0,
    input:0,
    contract:null
  }),
  methods:{
    async get(){
        if (window.ethereum) {
        window.web3 = new Web3(window.ethereum);
        this.connected = true;
      } else if (window.web3) {
        window.web3 = new Web3(window.web3.currentProvider);
      } else {
        window.alert("Non-Xinfin browser detected. You should consider trying XDCpay");
      }
      const web3 = window.web3;
      const accounts = await web3.eth.getAccounts();
      let accountBalance = await web3.eth.getBalance(accounts[0])
      console.log("accountBalance", accountBalance)
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
  }
}
  </script>