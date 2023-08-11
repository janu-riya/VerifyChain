<template>
  <v-container  class="personalform">
      <v-form v-model="formValid">
          <h4 class="text-center"> HSE Details</h4>
          <br/><br/><br/>
          <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Data insertion failed</v-alert>
          <v-row>
            <v-col cols="12" sm="6">
          <v-text-field label="Registration Number" outlined v-model="hse_regno" prepend-icon="mdi-notebook" :rules="[rules.required,rules.hse_regno]"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
          <v-text-field label="Marks in %" outlined v-model="hse_marks" prepend-icon="mdi-brightness-percent" :rules="[rules.required,rules.percents]"></v-text-field>
        </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
          <v-text-field label="School" outlined v-model="hse_school" prepend-icon="mdi-town-hall" :rules="[rules.required,rules.hse_school]"></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
         <v-text-field label="Board" outlined v-model="hse_board" prepend-icon="mdi-school" :rules="[rules.required,rules.hse_board]"></v-text-field>
        </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
         <v-select
         v-model="hse_passout"
         :items="hse_passout"
         label="Year of Completion"
         outlined
         :rules="[rules.required]"
         prepend-icon="mdi-calendar"
       ></v-select>
      </v-col>
      <v-col cols="12" sm="6">
          <v-file-input @change="fileselect"  label = "Upload Files" outlined :rules="[rules.required]" ></v-file-input>
        </v-col>
        </v-row>
          <v-container class="text-center">
          <v-btn text  @click="submit()" :disabled="!formValid" class ="button" color="blue lighten-1"> Submit </v-btn>
      </v-container>
      </v-form>
  </v-container>
</template>
<script>
export default{
  name: "hse",
  async mounted(){
      var url ='http://127.0.0.1:8000/user'
      this.generateYearRange();
      this.email= await this.$storage.getUniversal('Email');
      await this.$axios.get(url,{params:{email : this.email}}).then(res=>{
          this.name = res.data.name
      }).catch(error => console.log(error));

  },
  data:() =>({
      hse_regno : "",
      hse_marks : "",
      email: "",
      hse_school : '',
      fail: null,
      hse_board : '',
      formValid:null,
      rules : {
        required: (v) => !!v || "Required",
            percents : (v) => (v>=0 && v<=100) || "Value must be between 0 and 100",
            email : (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            name: (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in Name",
            hse_regno : (v) => v.match(/^[a-zA-Z0-9]+$/) || "Register number format is wrong",
            hse_school : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            hse_board : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters"
      },
      hse_passout: [],
  }),
  methods:{
      async fileselect(event){
    this.file=event
  },
      async submit(){
        let nurl = "http://127.0.0.1:8000/user/expupdation"
        let ndata={
          'email': this.email
        }
        let nres = await this.$axios.post(nurl, ndata)

          let url= "http://127.0.0.1:8000/hseupdate"
          let hdata = {
              hse_regno : this.hse_regno,
              email : this.email,
              name : this.name,
              hse_marks: this.hse_marks,
              hse_passout: this.hse_passout,
              hse_school: this.hse_school,
              hse_board : this.hse_board,


          }
          let result = await this.$axios.post(url,hdata);
          let formdata = new FormData()
            formdata.append('email',this.email)
            formdata.append('regno',this.hse_regno)
            formdata.append('file',this.file)
            let furl = "http://127.0.0.1:8000/uploadfile/S3"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
            if (result.data === res.data){
                this.$router.push('/user')
            }
            else{
                this.fail = true
            }
      },
      generateYearRange() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 50;

      for (let year = currentYear; year >= startYear; year--) {
        this.hse_passout.push(year);
      }
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