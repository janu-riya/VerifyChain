<template>
    <v-container>
      <br/><br/><br/><br/><br/><br/>
        <v-row align="center">
        <v-col cols="12" md="6">
          <v-card class="signin-card">
        <v-form>
            <h1 class="text-center"> Notary Signin </h1>
            <br><br>
            <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> Invalid Email ID or Password</v-alert>
            <v-row>
                <v-col cols="12">
              <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="email" prepend-icon="mdi-email" :rules="[rules.required,rules.email]" label ="Admin Email "></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field outlined :textarea="true" class="text-field-in-box" v-model="password" prepend-icon="mdi-lock" type="password" :rules="[rules.required]" label="Password"></v-text-field>
            </v-col>
            </v-row>
            <br>
            <v-row justify="center">
                <v-btn text @click="login()" color="blue lighten-1" width="200px">Signin</v-btn>
                </v-row>
        </v-form>
        </v-card> 
        </v-col>
        <v-col cols="14" md="6">
          <div class="blue-bubble">
            <img
              data-aos="zoom-in"
              class="guide2Image"
              data-aos-duration="800"
              data-aos-delay="100"
              src="https://png.pngtree.com/png-vector/20220825/ourmid/pngtree-administration-illustration-with-women-on-the-phone-and-talking-many-things-png-image_6122641.png"
              alt="Guide Image"
              :style="{ width: '100%', height: 'auto' }"

            />
          </div>
        </v-col>
        </v-row>
    </v-container>
</template>
<script>
export default{
    name :"notarylogin",
    data : () => ({
        email: "",
        password: "",
        fail: null,
        rules : {
            required: (v) => !!v || "Required",
            email : (v) => v.match(/\S+@\S+\.\S+/) || "Email format is wrong",
        }
    }),
    methods: {
        async login(){
          try{
            let url = "http://127.0.0.1:8000/notary/login"
            let nlogin = {
                email: this.email,
                password: this.password
            }
            let res = await this.$axios.get(url,{params:{'email': this.email, 'password': this.password}});
            this.$storage.setUniversal('notaryemail',this.email)

            let nurl = "http://127.0.0.1:8000/notary/logindate"
            let nres =  await this.$axios.post(nurl, nlogin)
            if(res.data == false){
              this.fail = true;
            }
            
            const access_token = res.data.access_token;
                if (access_token) {
                    // Save the access token to local storage or a secure cookie
                    localStorage.setItem('access_token', access_token);

                    // Redirect the user to the /user route
                    this.$router.push('/notary');
                  } else {
                    this.error = true;
                  }
          }catch (error) {
                  console.error('Error signing in:', error);
                  this.error = true;
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
