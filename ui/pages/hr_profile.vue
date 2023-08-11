<template>
  <v-main >
    <v-container v-if="isAuthenticated">
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
                  <hrprofile/>
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
  layout:'hr_layout',
  async mounted(){
      const accessToken = localStorage.getItem('access_token');
    this.isAuthenticated = !!accessToken;
    },
    data: () => ({
      isAuthenticated: false
    })

}
</script>
