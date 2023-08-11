<template>
  <v-main >
    <v-container>
      <v-row>
        <v-col>

            <v-container fluid >
              <v-card max-width="450px" class="mx-auto bg" style="border-color: blue;" elevation="5">
                <br><br>
                <v-row justify="center">
                  <v-col align-self="start" class="d-flex justify-center align-center pa-0" cols="12">
                    <v-avatar class="profile avatar-center-heigth avatar-shadow" color="grey" size="164">

                      <input ref="uploader" class="d-none" type="file" accept="image/*" :change="onFileChanged">
                      <v-img src="https://cdn.vuetifyjs.com/images/profiles/marcus.jpg"></v-img>


                    </v-avatar>

                  </v-col>
                  <v-btn @click="onButtonClick" class="upload-btn" x-large icon>
                    <v-icon>
                      mdi-camera
                    </v-icon>
                  </v-btn>
                </v-row>
                <vrow>
                  <nprofile/>
                </vrow>

              </v-card>
            </v-container>

        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
<script>
export default{
  name: 'profile',
  layout:'notary_layout',

  async mounted (){
      this.$vuetify.theme.dark =false;
      this.email = this.$storage.getUniversal('notaryemail')
      let url = "http://127.0.0.1:8000/notary"
      let res = await this.$axios.get(url,{params:{ email :this.email}});
      this.name=res.data.name
  },
  data: () =>({
      name : "Sajith Surendran",
      email:"",
  }),
 methods: {

 }
}
</script>
