<template>
  <v-app index>
    <v-app-bar app color="#3498db">
      <img class="mr-3" :src="require('../assets/blockedge-logo.svg')" height="40"/>
      <v-spacer></v-spacer>

      <!-- Desktop view (show buttons) -->
      <div class="hidden-sm-and-down">
        <a href="/">
          <v-btn text color="black" class="mr-2">Home</v-btn>
        </a>
        <a href="/aboutpage">
          <v-btn text color="black" class="mr-2">About</v-btn>
        </a>
        <a href="/featurespage">
          <v-btn text color="black" class="mr-2">Features</v-btn>
        </a>
        <a href="/contactpage">
          <v-btn text color="black" class="mr-2">Contact</v-btn>
        </a>
        <a href="/getstarted">
          <v-btn rounded color="blue lighten-5" class="text-white">Get Started</v-btn>
        </a>
      </div>

      <!-- Mobile view (show icon) -->
      <div class="hidden-md-and-up">
        <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item >
            <a href="/"><v-list-item-title>Home</v-list-item-title>
            </a>
          </v-list-item>
          <v-list-item >
            <a href="/aboutpage"><v-list-item-title>About</v-list-item-title>
            </a>
          </v-list-item>
          <v-list-item >
            <a href="/featurespage"><v-list-item-title>Features</v-list-item-title>
            </a>
          </v-list-item>
          <v-list-item >
            <a href="/contactpage"><v-list-item-title>Contact</v-list-item-title>
            </a>
          </v-list-item>
          <v-list-item >
            <a href="/getstarted"><v-list-item-title>Get Started</v-list-item-title>
            </a>
          </v-list-item>
        </v-list>
      </v-menu>
      </div>

    </v-app-bar>
    <v-main>
      <Nuxt/>
    </v-main>

    <v-footer color="#3498db" dark>
      <v-row justify="center" class="my-4 text-center">
        <v-col cols="12" style="color:black">
          Copyright @ Securekloud Technologies Ltd {{ new Date().getFullYear() }}
        </v-col>
        <v-col cols="12" style="width: 10%;">
          <v-btn style="width: 5%; color: black;" v-for="icon in icons" :key="icon" text dark>
            <v-icon>{{ icon }}</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="12" class="align-center" style="color:black">
          &copy; 2023 VerifiEdge
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'indexlayout',
  async mounted() {
    this.$vuetify.theme.dark = false;
  },
  data: () => {
    return {
      icons: ['mdi-facebook', 'mdi-twitter', 'mdi-instagram', 'mdi-youtube'],
      
    };
  },
  methods: {

  },
};
</script>

<style>
/* Add your custom styles here */
</style>
