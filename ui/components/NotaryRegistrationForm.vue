<template>
    <v-container class="personalform">
        <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Data insertion failed</v-alert>
        <v-form  v-model="formValid" >
                <br/>
                <h3 class="text-center"> Notary Registration Data</h3> <br />
                <br/><br/><br/>
                  <v-row>
                    <v-col>
                <v-text-field label="Name " prepend-icon="mdi-account" outlined v-model="name" :rules="[rules.required,rules.name]"></v-text-field>
            </v-col><v-col>
                <v-text-field label="Email" prepend-icon="mdi-email" outlined v-model="email" :rules="[rules.required,rules.email]"></v-text-field>
            </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                <v-text-field label="Enter the password" prepend-icon="mdi-lock" outlined v-model="password" type="password" :rules="[rules.required,rules.password]"></v-text-field>
            </v-col><v-col>
                <v-text-field label="Mobile Number" prepend-icon="mdi-phone" outlined v-model="mob" :rules="[rules.required,rules.mob]"></v-text-field>
            </v-col>
            </v-row>
            <v-row>
                <v-col>
                <v-text-field label="Aadhaar" prepend-icon="mdi-text-box" outlined v-model="aadhaar" :rules="[rules.required,rules.aadhaar]"></v-text-field>
            </v-col><v-col>
                <v-text-field label="PAN" prepend-icon="mdi-text-box" outlined v-model="pan" :rules="[rules.required,rules.pan]"></v-text-field>
            </v-col>
            </v-row>
                <v-container class="text-center">
                    <v-btn text color="blue lighten-1"  @click="submit()" :disabled="!formValid">submit</v-btn>
                </v-container>
        
        </v-form>
    </v-container>
</template>
<script>
export default {
    name: 'Notarydata',
    async mounted(){
        this.email =  this.$storage.getUniversal('Email');
        console.log(this.email);
    },
    data:() =>({
        name: "",
        email:"",
        password: "",
        mob:"",
        aadhaar : "",
        fail: null,
        pan:"",
        formValid:null,
        
        rules:{
            required: (v) => !!v || "Required",
            mob: (v) => v.match(/^[0-9]{10}$/) || "check your mobile number",
            aadhaar : (v) =>  v.match(/^\d{12}$/) || "Check the aadhaar number for errors",
            pan : (v) => v.match(/^([A-Z]){5}([0-9]){4}([A-Z]){1}?$/) || "Check the PAN number for errors",
            email : (v) => v.match(/\S+@\S+\.\S+/) || "Email format is wrong",
            name: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in Name",
            password: (v) =>  v.match(/^(?=.*[A-Z])(?=.*[@])(?=.*[a-z])(?=.*\d).{8,}$/)|| "Enter Password with One Cap letter ,@,small letter and with the number is required",

        }
    }),
    methods:{
        async submit(){
            let url = "http://127.0.0.1:8000/notary";
            let pdata= {
                name:this.name,
                email:this.email,
                password:this.password,
                mob : this.mob,
                aadhaar : this.aadhaar,
                pan : this.pan,
            }
            let result = await this.$axios.post(url, pdata);
            if (result.data == true){
                this.$router.push('/')
            }else{
                this.fail=true;
            }

        },
    },

}
</script>
<style>
.personalform{
    width: 50%;
}
</style>
