<template>
    <v-container class="personalform">
        <v-form v-model="formValid">
            <h3 class="text-center"> Last Experience Details</h3>
            <br/><br/><br/>
            <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Data insertion failed</v-alert>
            
            <v-row>
              <v-col cols="12">
                <v-text-field label="Employee ID" outlined
            prepend-icon="mdi-account-card"
            v-model="empid"
            :rules="[rules.required]"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
            <v-text-field label="Company Name" outlined prepend-icon="mdi-domain" v-model="company_name" :rules="[rules.required,rules.company_name]"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field label="HR Email" outlined prepend-icon="mdi-account-filter" v-model="hr_mail" :rules="[rules.required,rules.hr_mail]"></v-text-field>
          </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6">
            <v-menu v-model="startDatePicker" :close-on-content-click="false" :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on }">
                  <v-text-field v-model="start_date" prepend-icon="mdi-calendar" outlined label="Start Date" readonly v-on="on"></v-text-field>
                </template>
                <v-date-picker v-model="start_date" :max="today" no-title scrollable @input="saveStartDatePicker"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" sm="6">
              <v-menu v-model="endDatePicker" :close-on-content-click="false" :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on }">
                  <v-text-field v-model="end_date" prepend-icon="mdi-calendar" outlined label="End Date" readonly v-on="on"></v-text-field>
                </template>
                <v-date-picker v-model="end_date" :max="today" no-title scrollable @input="saveEndDatePicker"></v-date-picker>
              </v-menu>
            </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6">
            <v-text-field label="Designation" outlined prepend-icon="mdi-certificate" v-model="designation" :rules="[rules.required,rules.designation]"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field label="CTC (Cost To Company)" outlined prepend-icon="mdi-cash" v-model="lpa" :rules="[rules.required,rules.lpa]"></v-text-field>
          </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6">
            <v-text-field label="Reporting Manager" outlined prepend-icon="mdi-account-tie" v-model="reporting_manager" :rules="[rules.required,rules.reporting_manager]"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-file-input @change="fileselect" label="Experience Letter" outlined :rules="[rules.required]"></v-file-input>
          </v-col>
          </v-row>
            <v-container class="text-center">
                <v-btn text  @click="submit()" :disabled="!formValid" class="button" color="blue lighten-1"> Submit </v-btn>
            </v-container>
            <v-container v-if="notallowed" class="text-center">
              <v-alert  type="error" dismissible> Only pdf is allowed </v-alert>
            </v-container>

        </v-form>
    </v-container>
</template>
<script>
export default{
    name : "exp",
    async mounted(){
        var url ='http://127.0.0.1:8000/user'
        this.$vuetify.theme.dark =false;
        this.email= await this.$storage.getUniversal('Email');
        await this.$axios.get(url,{params:{email : this.email}}).then(res=>{
            this.name = res.data.name
        }).catch(error => console.log(error));

    },
    data : () => ({
        fail: null,
        empid :"",
        name: "",
        email:"",
        company_name:"",
        hr_mail: "",
        start_date:"",
        end_date:"",
        designation: "",
        lpa:"",
        reporting_manager:"",
        formValidator:null,
        notallowed: false,
        rules : {
            required: (v) => !!v || "Required",
            percents : (v) => (v>=0 && v<=100) || "Value must be between 0 and 100",
            email: (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            name: (v) => v.match(/^[A-Za-z\s]+$/) || 'No special characters in Name',
            empid: (v) => v.match(/^[A-Za-z0-9_-]{1,20}$/) || 'Emp ID format is wrong',
            company_name: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            hr_mail : (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            designation: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            lpa: (v) => v.match(/^[-+]?[0-9]*\.?[0-9]+$/) || 'lpa format is wrong',
            reporting_manager: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in name",
            date : (v) => (v.match(/^\d{2}\/\d{2}\/\d{4}$/)) || "Date format is not correct"
        },
      menu: false,
      today: new Date().toISOString().substring(0, 10),
      startDatePicker: false,
      endDatePicker: false,
    }),
    methods:{
        async fileselect(event){
      this.file=event
    },
     async submit(){
      

        
        let furl = "http://127.0.0.1:8000/uploadfile/S3"
        let formdata= new FormData()
        formdata.append('email',this.email)
        formdata.append('regno',this.empid)
        formdata.append('file',this.file)
        let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
        if(res.data.pdf == false){
              this.notallowed = true
            }
        if (res.data == true){
          let url="http://127.0.0.1:8000/exp"
          let edata = {
              empid : this.empid,
              name: this.name,
              email : this.email,
              company_name : this.company_name,
              hr_mail : this.hr_mail,
              start_date : this.start_date,
              end_date : this.end_date,
              designation : this.designation,
              lpa : this.lpa,
              reporting_manager: this.reporting_manager
          }
          let result = await this.$axios.post(url,edata);
          if(result.data == false){
                this.fail= true
            }
            else{
              let nurl = "http://127.0.0.1:8000/user/expupdation"
              let ndata={
                'email': this.email
              }
              let nres = await this.$axios.post(nurl, ndata)
              this.$router.push('/user')
            }
        }
            

     },
     saveStartDatePicker() {
      this.startDatePicker = false;
    },
    saveEndDatePicker() {
      this.endDatePicker = false;
    },
    getFormattedDate(date) {
      if (date) {
        const dateObj = new Date(date);
        const day = String(dateObj.getDate()).padStart(2, "0");
        const month = String(dateObj.getMonth() + 1).padStart(2, "0");
        const year = dateObj.getFullYear();
        return `${day}/${month}/${year}`;
      }
      return null;
    },

    }
}
</script>
<style>
.personalform {
  width: 100%;
  max-width: 600px; /* Adjust max-width as needed */
  margin: 0 auto;
  padding: 20px;
}
</style>