<template>
    <v-container>
      <v-card-text class="text-center" v-if="!formSubmitted">
        <v-btn  color="blue lighten-1" style="color:white; width:40;" @click="showForm = true" v-if="!formSubmitted">Add Address</v-btn>
      </v-card-text>
      <v-card-text v-else>
        <Addressviewpage/>
      </v-card-text>
  
      <v-dialog v-model="showForm" max-width="500px">
        
        <v-card>
          <v-card-title>
            <span class="headline">Address Form</span>
          </v-card-title>
  
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-row>
                <v-col>
              <v-text-field v-model="houseNo" prepend-icon="mdi-home" outlined label="House No/Name" :rules="[rules.required]"></v-text-field>
            </v-col><v-col>
              <v-text-field v-model="street" prepend-icon="mdi-road" outlined label="Street" :rules="[rules.required,rules.omg]"></v-text-field>
            </v-col>
            </v-row><v-row>
              <v-col>
              <v-text-field v-model="region" prepend-icon="mdi-home-group" outlined label="Town/City" :rules="[rules.required,rules.omg]"></v-text-field>
            </v-col><v-col>
              <v-text-field v-model="state" prepend-icon="mdi-flag" outlined label="State" :rules="[rules.required,rules.omg]"></v-text-field>
            </v-col>
            </v-row><v-row>
              <v-col>
              <v-text-field v-model="country" prepend-icon="mdi-earth" outlined label="Country" :rules="[rules.required,rules.omg]"></v-text-field>
            </v-col><v-col>
              <v-text-field v-model="zipcode" prepend-icon="mdi-map" outlined label="ZIP Code" :rules="[rules.required,rules.zipcode]"></v-text-field>
              </v-col>
            </v-row>
            </v-form>
          </v-card-text>
  
          <v-card-actions v-if="!formSubmitted" >
            <v-spacer></v-spacer>
            <v-btn color="error" text @click="showForm = false">Cancel</v-btn>
            <v-btn text color="blue lighten-1" :disabled="!valid" @click="submitForm()" class="button">Submit</v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>
    </v-container>
     
  
  </template>
  
  <script>
  export default {
    name:"Addaddress",
    async mounted(){
      this.email = this.$storage.getUniversal('Email');
    },
    data() {
      return {
        showForm: false,
        valid: false,
        formSubmitted: false,
        email:"",
        houseNo: "",
        street: "",
        region: "",
        state: "",
        country: "",
        zipcode: "",
        rules: {
          required:(v) => !!v || 'Required',
          zipcode: (v) => v.match(/^\d{6}$/) || 'Check your zipcode',
          omg :(v) => v.match(/^[A-Za-z\s]+$/) || 'Enter only characters',
          },
      };
    },
    methods: {
      async submitForm() {
        let url="http://127.0.0.1:8000/personal/address";
        let pdata={
          email: this.email,
          houseNo: this.houseNo,
          street: this.street,
          region: this.region,
          state: this.state,
          country: this.country,
          zipcode: this.zipcode,

        }
        let result = await this.$axios.post(url,pdata)
        if(result.data == true){
        
          this.showForm = false;
          this.formSubmitted = true;
        }
        else{
          this.fail=true;
        }
        },
      },
    };

  </script>
  