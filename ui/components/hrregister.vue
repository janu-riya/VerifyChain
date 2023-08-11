<template>
    <v-container >
        <v-row align="center">
            <v-col cols="10" md="6">
                <div class="blue-bubble">
            <img
              data-aos="zoom-in"
              class="guide2Image"
              data-aos-duration="800"
              data-aos-delay="100"
              src="https://d1idiaqkpcnv43.cloudfront.net/website1.0/images/sign-up.png"
              alt="Guide Image"
              :style="{ width: '130%', height: 'auto' }"
            />
          </div>
            </v-col>
             <v-col cols="12" md="6">
                <v-card class="signin-card">
                 <v-form v-model="isFormValid">
                    <h1 class="text-center" >Create your account</h1>
                      <v-alert dismissible type="error" v-model="fail"> Duplicate User Email </v-alert>

              <v-container class="text-center">
              </v-container>
             <br/>

            <v-row>
                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" required v-model="user.name" prepend-icon="mdi-account" label="Full Name" :rules="[rules.required, rules.name]"></v-text-field>
                </v-col>
            
                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="user.company_mail" prepend-icon="mdi-email" label="Company Email" :rules="[rules.required,rules.email]"></v-text-field>
                </v-col>

                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="user.company_reg" prepend-icon="mdi-notebook" label="Company Register Number" :rules="[rules.required,rules.company_reg]"></v-text-field>
                </v-col>

                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="user.mob" prepend-icon="mdi-phone" label="Mobile Number" :rules="[rules.required,rules.mob]"></v-text-field>
                </v-col>

                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="user.gst" prepend-icon="mdi-text-box" label="GSTIN Number" :rules="[rules.required,rules.gst]"></v-text-field>
                </v-col>
           
                <v-col cols="12">
                    <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="user.password" prepend-icon="mdi-lock" label="Password" type="password" :rules="[rules.required,rules.min]"></v-text-field>
                </v-col>
            </v-row>
            <br/>
        
        <v-row justify="center">

        <v-btn text  color="blue lighten-1" @click="submit()" :disabled="!isFormValid" > Submit</v-btn>
        </v-row>
        </v-form>
        <v-container v-if="sendotp">
            <v-form>
                <v-alert v-model="error" type="error"  dismissible>OTP verification failed</v-alert>
                <v-col>
                    <v-row>
                        <caption>Please enter the OTP below for verification</caption>
                    </v-row>
                    <v-row>
                        <v-text-field label ="Enter OTP Here" v-model="utop"></v-text-field>
                    </v-row>
                    <v-row>
                        <v-btn text  color="blue lighten-1" @click="signup()" >Signup</v-btn>
                    </v-row>
                </v-col>
            </v-form>
        </v-container>
                </v-card>
    </v-col>
        </v-row>
    </v-container>

</template>
<script>

export default{
name:'signuppage',
layout:'signinlayout',
async mounted(){
    this.$vuetify.theme.dark=false;
},
data:() => ({
    user :{
        name :'',
        company_reg: '',
        company_mail: '',
        password :'',
        mob:'',
        gst: '',        
        firstlogin :true,
        status: 'pending'
    },
    success:false,
    fail:false,
    otp:'',
    utop:'',
    isFormValid:null,
    error:false,
    sendotp:null,
    rules:{
        required: (v) => !!v || "Required",
        min : (v) =>  v.match(/^(?=.*[A-Z])(?=.*[@])(?=.*[a-z])(?=.*\d).{8,}$/)|| "Enter Password with One Cap letter ,@,small letter and with the number is required",
        email : (v) => v.match(/\S+@\S+\.\S+/) || "Email format is wrong",
        name: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in Name",
        mob: (v) => v.match(/^[0-9]{10}$/) || "check your mobile number",
        company_reg : (v) => v.match(/^\d{21}$/) || "Check the register number for errors",
        gst : (v) => v.match(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$/) || "Check the GSTN number for errors",
    }
}),
methods:{
    async home(){
        this.$router.push('/')
    },
    async submit(){
        let url = "http://3.84.79.77:8000/otp"
        let mdata = { params :{email : this.user.company_mail}}
        await this.$axios.get(url,mdata).then(res => {
            this.otp = res.data
            this.sendotp = true
            console.log(this.otp)
        }).catch(err => { console.log(err)});
    },
    async signup(){
        if (this.utop == this.otp){
            let url = "http://127.0.0.1:8000/hr"
            await this.$axios.post(url,this.user).then(res => {
                if (res.data == true){
                    this.success = true
                    this.$router.push('/hrsignin')
                }
                else{
                    this.fail = true
                }
            });
        }
        else {
            this.error = true
        }
    }
}
}
</script>
<style>
  
  .signin-card {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 40px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1)
  }
  
  .text-field-in-box {
    width: 100%;
  }
  
  .guide2Image {
    width: 100%;
    overflow: hidden;
  }

  .img-resize {
  max-width: 600%; 
  max-height: 600px;
  }
  
  @keyframes blueBubble {
    0% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-20px);
    }
    100% {
      transform: translateY(0);
    }
  }
  
  .blue-bubble {
    position: relative;
    display: inline-block;
    animation: blueBubble 2s infinite;
  }


</style>
