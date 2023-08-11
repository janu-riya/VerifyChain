<template>
    <v-container class="text-center" style="padding: 2%;">
      <v-text> <h1 style="text-align: center;" class="font-bold text-white text-5xl">Who need us?</h1></v-text>
      <br>
          <br><br>
          <v-row>
              <v-col>
                <v-row justify="center">
                  <v-img src="https://media.istockphoto.com/id/499383695/photo/group-of-futuristic-office-skyscrapers-on-white-background.jpg?s=612x612&w=0&k=20&c=dRrFQLvXIM3K4Dszj-LvunkRkygoP94R8dPT0ZNcbOI="  height="200px" max-width="200px" />
                </v-row>
                <br><br>
                <v-row justify="center">
                  <v-icon color="blue lighten-1"  >mdi-office-building-outline</v-icon>
                  <v-btn text color="blue lighten-1" width="100px" @click="hr()"> Companies </v-btn>
                </v-row>

              </v-col>
              <v-col>
                <v-row justify="center">
                  <v-img src="https://media.istockphoto.com/id/1440206251/vector/testament-and-last-will-documents-signing-notary-and-official-testamentary-banner.jpg?s=612x612&w=0&k=20&c=72Knc193VZH7Qw7YYlfXNvdb5ZWhnEkJImB_XH8WAfA=" height="200px" max-width="200px" />
                </v-row>
                <br><br>
                <v-row justify="center">
                  <v-icon color="blue lighten-1">mdi-certificate-outline</v-icon>
                  <v-btn text color="blue lighten-1" width="100px" @click="notary()"> Admin </v-btn>
                </v-row>

              </v-col>
              <v-col>
                <v-row justify="center">
                  <v-img src="https://i.ibb.co/GsHhLK0/15-Best-Digital-Agency-Websites-removebg-preview.png" height="200px" max-width="200px" />
                </v-row>
                <br><br>
                <v-row justify="center">
                  <v-icon color="blue lighten-1"  >mdi-account</v-icon>
                  <v-btn text color="blue lighten-1" width="100px" @click="agencies()"> Agencies</v-btn>
                </v-row>
                

              </v-col>
          </v-row>
      </v-container>
</template>
<script>
export default {
    name:'whoneedsus',
    data:()=>({

    }),
    methods: {

       async hr() {
           this.$router.push("/hrsignin");
       },
       async agencies(){
         this.$router.push("/hrsignin");
       },
       async notary(){
         this.$router.push("/notarysignin");
       }
   },
}
</script>
