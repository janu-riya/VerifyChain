<template>
    <v-container class="personalform">
        <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Data insertion failed</v-alert>
        <v-form  v-model="formValid">
                <br/>
                <h3 class="text-center"> Company Registration Data</h3> <br />
                <br/><br/><br/>
                <v-text-field label="Company Name " prepend-icon="mdi-domain" outlined v-model="company" :rules="[rules.required]"></v-text-field>
                <v-row>
                    <v-col>
                <v-text-field label="Company Registration Number" prepend-icon="mdi-notebook" outlined v-model="company_reg" :rules="[rules.required,rules.company_reg]"></v-text-field>
                </v-col><v-col>
                <v-text-field label="Company Email" prepend-icon="mdi-email" outlined v-model="company_mail" :rules="[rules.required,rules.email]"></v-text-field>
                </v-col>
                </v-row>
                <v-row>
                    <v-col>
                <v-text-field label="Enter the password" prepend-icon="mdi-lock" outlined v-model="password" type="password" :rules="[rules.required,rules.password]"></v-text-field>
            </v-col><v-col>
                <v-text-field label="Phone Number" prepend-icon="mdi-phone" outlined v-model="mob" :rules="[rules.required,rules.mob]"></v-text-field>
            </v-col>
               </v-row>
               <v-row>
                <v-col>
                <v-text-field label="GSTN Number" prepend-icon="mdi-text-box" outlined v-model="gst" :rules="[rules.required,rules.gst]"></v-text-field>
                </v-col><v-col>
                <v-file-input @change="fileselect" label="Upload GSTN Certificate File" outlined :rules="[rules.required]"></v-file-input>
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
    name: 'Companydata',
    async mounted(){
        this.email =  this.$storage.getUniversal('Email');
        console.log(this.email);
    },
    data:() =>({
        company :"",
        company_reg: "",
        company_mail:"",
        password: "",
        mob:"",
        gst:"",
        formValid:null,
        rules:{
            required: (v) => !!v || "Required",
            mob: (v) => v.match(/^[0-9]{10}$/) || "check your mobile number",
            company_reg : (v) => v.match(/^\d{21}$/) || "Check the register number for errors",
            gst : (v) => v.match(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$/) || "Check the GSTN number for errors",
            email : (v) => v.match(/\S+@\S+\.\S+/) || "Email format is wrong",
            password: (v) =>  v.match(/^(?=.*[A-Z])(?=.*[@])(?=.*[a-z])(?=.*\d).{8,}$/)|| "Enter Password with One Cap letter ,@,small letter and with the number is required",
            name: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in Name",
            alphnum: (v) => v.match(/^[A-Za-z0-9\s]+$/) || "No special Characters",
            date : (v) => (v.match(/^\d{2}\/\d{2}\/\d{4}$/)) || "Date format is not correct"
  
        }
    }),
    methods:{
      async fileselect(event){
      this.file=event
    },
        async submit(){
            let url = "http://127.0.0.1:8000/hr";
            let pdata= {
                name : this.company,
                company_reg : this.company_reg,
                company_mail : this.company_mail,
                password : this.password,
                mob : this.mob,
                gst : this.gst,
            }
            let result = await this.$axios.post(url, pdata);
            if (result.data == true){
                this.$router.push('/ ')
            }else{
                this.fail=true;
            }
            let formdata = new FormData()
            formdata.append('company_mail',this.company_mail)
            formdata.append('file',this.file)
            let furl="http://127.0.0.1:8000/uploadgstn"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
            if (result.data == res.data){
                this.$router.push('/')
            }else{
                this.fail= true
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