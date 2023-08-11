<template>
  <v-container class="personalform">
    <v-alert border="top" color="red lighten-1" dismissible v-if="fail">Data insertion failed</v-alert>
    <v-form v-model="isFormValid">
      <br />
      <h3 class="text-center">Personal Data</h3>
      <br/><br/><br/>
      <v-row>
        <v-col cols="12">      
          <v-text-field label="Employee ID" v-model="empid" outlined prepend-icon="mdi-account-card" :rules="[rules.required, rules.alphnum]"></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
      <v-menu v-model="DatePicker" :close-on-content-click="false" :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
        <template v-slot:activator="{ on }">
          <v-text-field v-model="doj" outlined prepend-icon="mdi-calendar" label="Date of Joining" readonly v-on="on"></v-text-field>
        </template>
        <v-date-picker v-model="doj" :max="today" no-title scrollable @input="saveDatePicker"></v-date-picker>
      </v-menu>
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field label="Company Name" outlined v-model="company" prepend-icon="mdi-domain" :rules="[rules.required,rules.company]"></v-text-field>
    </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
      <v-text-field label="Designation" outlined v-model="designation" prepend-icon="mdi-certificate" :rules="[rules.required, rules.designation]"></v-text-field>
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field label="Company Email" outlined v-model="company_email" prepend-icon="mdi-email" :rules="[rules.required, rules.email]"></v-text-field>
    </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
      <v-text-field label="Mobile Number" outlined v-model="mob" prepend-icon="mdi-phone" :rules="[rules.required, rules.mob]"></v-text-field>
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field label="Aadhaar" outlined v-model="aadhaar" prepend-icon="mdi-text-box" :rules="[rules.required, rules.aadhaar]"></v-text-field>
    </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
      <v-text-field label="PAN" outlined v-model="pan" prepend-icon="mdi-text-box" :rules="[rules.required, rules.pan]"></v-text-field>
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field label="Passport" outlined v-model="passport" prepend-icon="mdi-text-box" :rules="[rules.required,rules.passport]"></v-text-field>
    </v-col>
    </v-row>
      <v-container class="text-center">
        <v-btn text color="blue lighten-1" @click="submit()" :disabled="!isFormValid" class="button">Submit</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'personaldata',
  async mounted() {
    this.email = this.$storage.getUniversal('Email');
    console.log(this.email);
  },
  data() {
    return {
      empid: "",
      doj: "",
      email: "",
      designation: "",
      company: "",
      company_email: "",
      mob: "",
      aadhaar: "",
      fail: null,
      pan: "",
      passport: "",
      isFormValid: null,
      rules: {
        required: (v) => !!v || "Required",
            mob: (v) => v.match(/^[0-9]{10}$/) || "check your mobile number",
            aadhaar : (v) =>  v.match(/^\d{12}$/) || "Check the aadhaar number for errors",
            pan : (v) => v.match(/^([A-Z]){5}([0-9]){4}([A-Z]){1}?$/) || "Check the PAN number for errors",
            designation : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            email : (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            company: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            empid : (v) => v.match(/^[A-Za-z0-9_-]{1,20}$/) || 'Emp ID format is wrong',
            passport : (v) => v.match(/^[A-Za-z0-9]{6,15}$/) || "Passport format is wrong",
            company_email : (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            alphnum: (v) => v.match(/^[A-Za-z0-9\s]+$/) || "No special Characters",
            date : (v) => (v.match(/^\d{2}\/\d{2}\/\d{4}$/)) || "Date format is not correct"
      },
      menu: false,
      today: new Date().toISOString().substring(0, 10),
      DatePicker: false,
    };
  },
  methods: {
    async submit() {
      let nurl = "http://127.0.0.1:8000/user/expupdation"
        let ndata={
          'email': this.email
        }
        let nres = await this.$axios.post(nurl, ndata)
      let url = 'http://127.0.0.1:8000/personal/update';

      let pdata = {
        empid: this.empid,
        doj: this.doj,
        email: this.email,
        designation: this.designation,
        company_name: this.company,
        company_mail: this.company_email,
        mob: this.mob,
        aadhaar: this.aadhaar,
        pan: this.pan,
        passport: this.passport,
      };
      let result = await this.$axios.post(url, pdata);
      if (result.data === true) {
        this.$router.push('/user');
      } else {
        this.fail = true;
      }
    },
    saveDatePicker() {
      this.DatePicker = false;
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
  },
};
</script>

<style>
.personalform {
  width: 100%;
  max-width: 600px; /* Adjust max-width as needed */
  margin: 0 auto;
  padding: 20px;
}
</style>