<template>
    <v-app>
        <v-app-bar app color="indigo darken-4">
            <v-app-bar-title style="color: antiquewhite;">Payments</v-app-bar-title>
        </v-app-bar>
        <v-main>
            <v-container style="width: 50%;margin: 10% auto;">
                <h3 class="text-h6"> Payment Receipt </h3><br/>
                <h3 class="text-subtitle-1"> Data Charges : INR 100 </h3>
                <h3 class="text-subtitle-1"> Platform Service Charges : INR 100 </h3>
                <h3 class="text-subtitle-1"> Blockchain Service Charges : INR 100</h3>
                <h3 class="text-subtitle-1"> Total : INR 300 </h3>
                <br/>
                <v-btn @click="pay()" width="100px" color="success">Pay</v-btn>
                <v-btn @click="decline()" width="100px" color="error">Decline</v-btn>
            </v-container>
        </v-main>
    </v-app>
</template>
<script>
export default{
    name:"payment",
    async mounted(){
        this.$vuetify.theme.dark=false
        this.email = await this.$storage.getUniversal('user_email')
        this.hr_email = await this.$storage.getUniversal('hrmail');
        let url = "http://127.0.0.1:8000/hrprofile";
        let hr={
            'company_mail': this.hr_email,
        }
        let result= await this.$axios.post(url,hr);
        this.hr_name = result.data.name
    },
    data:()=>({
        email :"",
        hr_email : '',
        hr_name:"",
    }),
    methods:{
        async pay(){
            let url="http://127.0.0.1:8000/requestdata"
            let requestdata = {
                user_email : this.email,
                hr_email : this.hr_email,
                hr_name : this.hr_name,
            }
            let res = await this.$axios.post(url,requestdata);
            if(res.data == true){
                console.log("request updates")
                this.$router.push('/hrpage')
            }
            
        },
        async decline(){
            this.$router.push("/hrpage");
        }
    }

}
</script>