<template>
  <v-container class="signin">
    <v-row align="center">
      <v-col cols="14" md="6">
        <div class="blue-bubble">
          <img
            data-aos="zoom-in"
            class="guide2Image"
            data-aos-duration="800"
            data-aos-delay="100"
            src="https://www.naxeed.com/themes/default/images/login-img.png"
            alt="Guide Image"
            :style="{ width: '100%', height: 'auto' }"
          />
        </div>
      </v-col>
      <v-col cols="12" md="6">
        <v-card elevation="12" class="signin-card">
          <v-form>
            <h1 class="text-center">User Login</h1>
            <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Invalid Email ID or Password</v-alert>

            <div v-if="error" class="custom-info">
            <v-icon class="alert-icon">mdi-alert-circle</v-icon>
            <span class="alert-text">Login Failed</span>
          </div>
            

            <v-container class="text-center">
            </v-container>

            <br />

            <v-row>
              <v-col cols="12">
                <v-text-field
                  outlined
                  :textarea="true"
                  class="text-field-in-box"
                  v-model="signindata.email"
                  prepend-icon="mdi-email"
                  :rules="[rules.email, rules.required]"
                  label="Personal Email"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  outlined
                  :textarea="true"
                  class="text-field-in-box"
                  v-model="signindata.password"
                  prepend-icon="mdi-lock"
                  type="password"
                  :rules="[rules.required]"
                  label="Password"
                ></v-text-field>
              </v-col>
            </v-row>

            <br />

            <v-row justify="center">
              <v-col cols="12">
                <v-btn text color="blue lighten-1" @click="signin()">Sign In</v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default{
  name : 'usersignin',
  async mounted(){
      this.$vuetify.theme.dark=false;
  },
  data: () =>({
    return:{
      email:'',
      password:'',
    },
      signindata : {
          email : '',
          password :'',
          firstlogin : null,

      },
      error : false,
      fail: false,

      rules : {
          required: (v) => !!v || "Required",
          email : (v) => v.match(/\S+@\S+\.\S+/) || "Email format is wrong",
      }
  }),
  methods :{
      async signin(){
        try{
          let url= 'http://127.0.0.1:8000/login'
              let res = await this.$axios.get(url, {params:{'email':this.signindata.email, 'password': this.signindata.password}})
              this.email = this.$storage.setUniversal('Email',this.signindata.email)
              this.gmail = this.$storage.setUniversal('login_mail', this.signindata.email)
              console.log(this.email)
              if(res.data == false){
                this.fail = true;
              }
              const access_token = res.data.access_token;
              if (access_token) {
                  // Save the access token to local storage or a secure cookie
                  localStorage.setItem('access_token', access_token);

                  // Redirect the user to the /user route
                  this.$router.push('/user');
                } 
          }catch (error) {
                console.error('Error signing in:', error);
                this.error = true;
              }
          }
      },
  }

</script>
<style>
.signin {
  margin-top: 5vh;
  margin-bottom: 5vh;
  text-align: center;
}

.signin-card {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 40px;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
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

.custom-info{
  display: flex;
  align-items: center;
  background-color: transparent;
  color: red;
}

.custom-info .alert-icon {
  margin-right: 5px;
  color:red;

}

.custom-info .alert-text{
  font-size:16px;
}
</style>
