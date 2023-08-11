<template>
<v-container v-if="isAuthenticated">
  <br>
  <hrindex/>
  <profileapprove/>
</v-container>
</template>
<script>
export default{
    layout:"hr_layout",
    async mounted(){
      const accessToken = localStorage.getItem('access_token');
    this.isAuthenticated = !!accessToken;
    },
    data: () => ({
      isAuthenticated: false
    })

}
</script>
