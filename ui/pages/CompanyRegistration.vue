<template>
    <v-container >
        <CompanyRegistrationForm/>
    </v-container>
</template>
<script>
export default {
name: 'CompanyRegistration',
layout:'datacollection',
async mounted(){
    this.$vuetify.theme.dark=false;
},
data: () => ({
}),
methods:{
   
    async home(){
    }

}
}
</script>
<style>
.form{
width: 55% ;

}
</style>