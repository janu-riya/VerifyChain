<template>
    <v-container >
        <notarylogin/>
    </v-container>
</template>
<script>
export default{
    name: "notarysignin",
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

