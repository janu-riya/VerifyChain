<template>


  <v-container style="width: 80%; ">

        <v-container>
          <v-row>
            <v-col style="padding-left: 4%;">
              <h3 class="text-title-1">Name</h3>
              <h3 class="text-subtitle-1">{{ pdata.name }}</h3>
              <h3 class="text-title-1">Email</h3>
              <h3 class="text-subtitle-1">{{ pdata.company_mail }}</h3>
              <h3 class="text-title-1">Emplyee ID</h3>
              <h3 class="text-subtitle-1">{{ pdata.empid }}</h3>

            </v-col>


          </v-row>
        </v-container>


  </v-container>
</template>

<script>
export default{
name: 'hrprofile',
async mounted (){
  this.$vuetify.theme.dark =false;
  this.company_mail = this.$storage.getUniversal('hrmail')
  let url = "http://127.0.0.1:8000/hr"
  let res = await this.$axios.get(url,{params:{ company_mail :this.company_mail}});
  this.pdata=res.data
  console.log(this.pdata)


},
data: () =>({
  company_mail:"",
  pdata :{},

}),
}
</script>
