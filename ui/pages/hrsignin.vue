<template>
    <v-container >
        <hrlogin/>
    </v-container>
</template>
<script>
export default{
    name: "hrsignin",
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

