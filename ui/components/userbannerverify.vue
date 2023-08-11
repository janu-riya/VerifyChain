
<template>
  <v-container  style="width: 100%;">
    <v-row>
      <v-container v-if="pending" class="text-center">
        <v-icon size="180px" color="yellow" ></v-icon>
      </v-container>
      <v-container v-if="verified" class="text-center">
        <v-icon size="150px" color="green">mdi-check-decagram</v-icon>
      </v-container>
      <v-container v-if="rejected" class="text-center">
        <v-icon size="150px" color="red">mdi-cancel</v-icon>
      </v-container>
    </v-row>
    <v-row>
      <v-container class="text-center" fluid>
        <v-responsive :aspect-ratio="16 / 9">
          <v-btn color="blue lighten-1" style="color:white;" @click="approve(data.email)">Approve</v-btn>&emsp;
          <v-btn color="blue lighten-1" style="color:white;" @click="deny(data.email)">Reject</v-btn>
        </v-responsive>

      </v-container>
    </v-row>
  </v-container>

</template>
<script>
export default {
  name:"userbanner",
  async mounted(){
      this.email = this.$storage.getUniversal('user_email')
      console.log(this.email)
      let url = "http://127.0.0.1:8000/user"
      let res = await this.$axios.get(url,{params:{ email :this.email}});
      this.data=res.data

      this.notary = this.$storage.getUniversal('notaryemail')
       let nurl = "http://127.0.0.1:8000/notary"
        let nres = await this.$axios.get(nurl,{params:{email: this.notary}})
        this.ndata = nres.data

        if (this.data.status == "pending"){
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
  data:()=>({
      name:"",
      email:"",
      data:{},
      pending: false,
      error:false,
      verified: false,
      rejected: false

  }),
  methods:{
    async approve(email){
      let url = "http://127.0.0.1:8000/verify/user"
      let vdata={
        user_email: email,

        notary_email: this.ndata.email,
        notary_name: this.ndata.name
      }
      let res = await this.$axios.post(url, vdata)
      console.log(res.data)

    },
    async deny(email){
        console.log(email)
        let url = "http://127.0.0.1:8000/verify/user"
        let reject={
          user_email: email,
          notary_email: this.ndata.email,
          notary_name: this.ndata.name,
          status: "rejected"
        }
        let res = this.$axios.post(url,reject)
    }
   }
}
</script>
