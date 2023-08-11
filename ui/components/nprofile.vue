<template>


  <v-container style="width: 80%; ">

        <v-container>
          <v-row>
            <v-col style="padding-left: 4%;">
              <h3 class="text-title-1">Name</h3>
              <h3 class="text-subtitle-1">{{ pdata.name }}</h3>
              <h3 class="text-title-1">Email</h3>
              <h3 class="text-subtitle-1">{{ pdata.email }}</h3>

            </v-col>


          </v-row>
        </v-container>


  </v-container>
</template>

<script>
export default{
name: 'nprofile',
async mounted (){
  this.$vuetify.theme.dark =false;
  this.email = this.$storage.getUniversal('notaryemail')
  let url = "http://127.0.0.1:8000/notary"
  let res = await this.$axios.get(url,{params:{ email :this.email}});
  this.pdata=res.data
  console.log(this.pdata)


},
data: () =>({
  email:"",
  pdata :{},

}),
}
</script>
