<template>
  <v-container  class="signin" >
      <admin/>
  </v-container>
</template>
<script>
export default{
  name: "super_admin",
  layout:'signinlayout',
  async mounted(){
      this.$vuetify.theme.dark=false;
  },
  data: () => ({

  }),
  methods:{
      async home(){
          this.$router.push('/');
      },
  }
}
</script>
<style>
.signin{
  width: 30%;
  margin: 0% auto;
  text-align: center;
}
</style>
