<template>
  <v-container>
    <br>
      <v-container>
          <h1 style="color: rgb(4, 4, 8);">Notary Requests</h1>
          <br/><br/>
        <v-row>
          
          <v-col>
            <v-card>

              <v-card-title>PENDING REQUESTS</v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count }}</h1></v-card-title>
              <v-card-actions>
                <v-btn
                  text
                  color="indigo darken-4"
                  @click="reveal = true"
                >
                  Show
                </v-btn>
              </v-card-actions>
              <v-expand-transition>
                <v-card
                  v-if="reveal"
                  class="transition-fast-in-fast-out v-card--reveal"
                  style="height: 100%;"
                >
                  <NotaryPending/>
                  <v-card-actions class="pt-0">
                    <v-btn
                      text
                      color="red"
                      @click="reveal = false"
                    >
                      Close
                    </v-btn>
                  </v-card-actions>
                </v-card>

              </v-expand-transition>
            </v-card>

          </v-col>
          <v-col>
            <v-card>
              <v-card-title>APPROVED REQUESTS</v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count1 }}</h1></v-card-title>
            <v-card-actions>
              <v-btn
                text
                color="indigo darken-4"
                @click="approve = true"
              >
                Show
              </v-btn>
            </v-card-actions>
            <v-expand-transition>
              <v-card
          v-if="approve"
          class="transition-fast-in-fast-out v-card--reveal"
          style="height: 100%;"
        >

            <NotaryyApproved/>


          <v-card-actions class="pt-0">
            <v-btn
              text
              color="red"
              @click="approve = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
            </v-expand-transition>
          </v-card>
          </v-col>

        </v-row>

      </v-container>
      <v-container>
          <h1 style="color: rgb(4, 4, 8);">Company Requests</h1>
          <br/><br/>
        <v-row>
          
          <v-col>
            <v-card>

              <v-card-title>PENDING REQUESTS</v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count }}</h1></v-card-title>
              <v-card-actions>
                <v-btn
                  text
                  color="indigo darken-4"
                  @click="reveal1 = true"
                >
                  Show
                </v-btn>
              </v-card-actions>
              <v-expand-transition>
                <v-card
                  v-if="reveal1"
                  class="transition-fast-in-fast-out v-card--reveal"
                  style="height: 100%;"
                >
                  <CompanyPending/>
                  <v-card-actions class="pt-0">
                    <v-btn
                      text
                      color="red"
                      @click="reveal1 = false"
                    >
                      Close
                    </v-btn>
                  </v-card-actions>
                </v-card>

              </v-expand-transition>
            </v-card>

          </v-col>
          <v-col>
            <v-card>
              <v-card-title>APPROVED REQUESTS</v-card-title>
              <v-card-title><h1 style="font-weight: normal; font-size: 70px;" >{{ count1 }}</h1></v-card-title>
            <v-card-actions>
              <v-btn
                text
                color="indigo darken-4"
                @click="approve1 = true"
              >
                Show
              </v-btn>
            </v-card-actions>
            <v-expand-transition>
              <v-card
          v-if="approve1"
          class="transition-fast-in-fast-out v-card--reveal"
          style="height: 100%;"
        >

            <CompanyApproved/>


          <v-card-actions class="pt-0">
            <v-btn
              text
              color="red"
              @click="approve1 = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
            </v-expand-transition>
          </v-card>
          </v-col>

        </v-row>

      </v-container>



  </v-container>
</template>
<script>
export default {
  name :"SuperAdminRequests",
  layout: "SuperAdmin_layout",
  async mounted(){
    this.$vuetify.theme.dark =false;
    let url = "http://127.0.0.1:8000/notary/pending"
        let res = await this.$axios.get(url)
        this.datas = res.data.list
        this.count = res.data.count

    let surl = "http://127.0.0.1:8000/notary/verified"
    let sres = await this.$axios.get(surl)
    this.count1 = sres.data.count1

    let Eurl = "http://127.0.0.1:8000/company/pending"
        let Eres = await this.$axios.get(Eurl)
        this.infos = Eres.data.list
        this.count = Eres.data.count

    let Gurl = "http://127.0.0.1:8000/company/verified"
    let Gres = await this.$axios.get(Gurl)
    this.count1 = Gres.data.count1

  },
  data: () => ({
      reveal: false,
      approve: false,
      reveal1: false,
      approve1: false,
      count:{},
      count1:{},
      counts:{}
    }),

}
</script>

