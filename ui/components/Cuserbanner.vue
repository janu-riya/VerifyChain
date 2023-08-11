
<template>
  <v-container  style="width: 80%;">
    <v-card-title>  {{ name }}</v-card-title>
    <v-card-subtitle>

      {{ email }}
    </v-card-subtitle>

  </v-container>
</template>
<script>
export default {
  name:"userbanner",
  async mounted(){
      this.email = this.$storage.getUniversal('search_email')
      console.log(this.email)
      let url = "http://127.0.0.1:8000/user"
      let res = await this.$axios.get(url,{params:{ email :this.email}});
      this.name=res.data.name
  },
  data:()=>({
      name:"",
      email:"",

  }),
}
</script>
