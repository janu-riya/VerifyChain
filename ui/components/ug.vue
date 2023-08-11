<template>
    <v-container class="personalform">
        <v-form v-model="formValid">
            <h4 class="text-center"> UG Details</h4>
            <br/><br/><br/>
            <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Data insertion failed</v-alert>
            <v-text-field label="Registration Number" outlined v-model="ug_regno" prepend-icon="mdi-notebook" :rules="[rules.required,rules.ug_regno]"></v-text-field>
          <v-row>
            <v-col cols="12" sm="6">
          <v-text-field label="Marks in %" outlined v-model="ug_marks" prepend-icon="mdi-brightness-percent" :rules="[rules.required,rules.percents]"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
          <v-text-field label="Specialization" outlined v-model="ug_specialization" prepend-icon="mdi-school" :rules="[rules.required,rules.ug_specialization]"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
          <v-text-field label="College" outlined v-model="ug_college" prepend-icon="mdi-town-hall" :rules="[rules.required,rules.ug_college]"></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field label="University" outlined v-model="ug_university" prepend-icon="mdi-school" :rules="[rules.required,rules.ug_university]"></v-text-field>
        </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
          <v-select
          v-model="ug_passout"
          :items="ug_passout"
          label="Year of Completion"
          outlined
          :rules="[rules.required]"
          prepend-icon="mdi-calendar"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="6">
          <v-file-input @change="fileselect" label="Upload File" outlined :rules="[rules.required]"></v-file-input>
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
    name: "ug",
    async mounted(){
        var url ='http://127.0.0.1:8000/user'
        this.generateYearRange();
        this.email= await this.$storage.getUniversal('Email');
        await this.$axios.get(url,{params:{email : this.email}}).then(res=>{
            this.name = res.data.name
        }).catch(error => console.log(error));

    },
    data:() =>({
        ug_regno : "",
        email : "",
        fail:null,
        name : "",
        ug_specialization : "",
        ug_college:"",
        ug_marks:"",
        ug_university:"",
        formValid:null,
        notallowed: false,
        rules : {
            required: (v) => !!v || "Required",
            percents : (v) => (v>=0 && v<=100) || "Value must be between 0 and 100",
            email : (v) => v.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) || "Email format is wrong",
            name : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters in Name",
            ug_regno : (v) => v.match(/^[a-zA-Z0-9]+$/) || "Register number format is wrong",
            ug_specialization : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            ug_college : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
            ug_university : (v) => v.match(/^[A-Za-z\s]+$/) || "No special Characters",
        },
        ug_passout: [],
    }),
    methods:{
        async fileselect(event){
      this.file=event
    },
        async submit(){
            
            let formdata = new FormData()
            formdata.append('email',this.email)
            formdata.append('regno',this.ug_regno)
            formdata.append('file',this.file)
            let furl="http://127.0.0.1:8000/uploadfile/S3"
            let res = await this.$axios.post(furl,formdata,{ headers : {'Content-Type': 'application/json',}});
            if(res.data.pdf == false){
              this.notallowed = true
            }
            if (res.data == true){
              let url="http://127.0.0.1:8000/ug"
            let udata={
                ug_regno : this.ug_regno,
                email : this.email,
                name : this.name,
                ug_specialization : this.ug_specialization,
                ug_college : this.ug_college,
                ug_marks : this.ug_marks,
                ug_passout : this.ug_passout,
                ug_university : this.ug_university
            }
            let result = await this.$axios.post(url,udata);
            if(result.data == false){
                this.fail= true
            }
            else{
              this.$router.push('/user')
            }
            }

        },
        generateYearRange() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 50;

      for (let year = currentYear; year >= startYear; year--) {
        this.ug_passout.push(year);
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