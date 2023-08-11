<template>
    <v-app>
        <v-app-bar app color="indigo darken-3"> 
           <v-btn icon @click="home()" ><v-icon color="white">mdi-home</v-icon></v-btn>
           <h3 class="white--text"> Experience Verification</h3>
        </v-app-bar>
        <v-main>
            <v-container class="search" v-if="searchbox">
                <v-text-field label="Employee ID" v-model="empid"></v-text-field>
                <v-container class="text-center">
                    <v-btn text @click="fetchdata()" width="200px" color="indigo darken-2">Fetch</v-btn>
                </v-container>
                <v-alert border="top" color="red lighten-1" dismissible  v-if="fail"> No Data Found</v-alert>
            </v-container>
            <v-container class="personalform" v-if="data">
                <v-card >
                    <br/>
                    <h3 class="indigo--text text--lighten-2 text-center"> Employment Data </h3> 
                    <br/>
                <v-card-title>
                Employee ID&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;:&emsp;{{ empid }} <br />
                Name&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;:&emsp;{{ name }} <br/>
                Designation&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;:&emsp;{{ designation }} <br/>
                Company Name&emsp; &emsp;&emsp;&emsp;&ensp;:&emsp;{{ company}}  <br/>
                Start Date&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;:&emsp;{{ start_date }}  <br/>
                End Date&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;:&emsp;{{ end_date }}  <br/>
                Reporting Manager&emsp;&nbsp;&emsp;&emsp;:&emsp;{{ reporting_manager}} <br/>
                CTC&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&emsp;:&emsp;{{ lpa}}LPA<br/>
            </v-card-title>
            <v-card-actions>
                <v-btn text @click="accept()"  width="200px" color="indigo darken-2"> Approve</v-btn>
                <v-spacer></v-spacer>
                <v-btn text @click="refuse()" width="200px" color="red lighten-2"> Reject</v-btn>
            </v-card-actions>
                </v-card>
            </v-container><br/><br/>
            <v-container class="personalform" v-if="user">
                <v-form >
                    <h3 class="red--text text-center"> Employee Name&emsp;: &emsp;{{ name }}</h3> 
                    <v-text-field label="Reason for leaving" v-model="reason"></v-text-field>
                    <v-select :items="option" label="Eligiblility for rehire" v-model="rehire"></v-select> 
                    <v-select :items="option" label="Is there any pending dues ?" v-model="dues"></v-select>
                    <v-select :items="option" label="Is the candidate officially relieved ?" v-model="relieved"></v-select> 
                    <v-text-field label="Remarks" v-model="remarks"></v-text-field>
                    <v-container class="text-center">
                        <v-btn text @click="update()" color="indigo darken-2">Update</v-btn>
                    </v-container>
                </v-form>
            </v-container><br/><br/>
            <v-container v-if="approve">
                <v-alert border="top" color="teal lighten-2" dismissible v-if="approve"> Verification Success! You can close the tab</v-alert>
            </v-container><br/><br/>
            <v-container v-if="reject">
                <v-alert border="top" color="red lighten-2" dismissible v-if="reject"> Data Rejected ! You can close the tab</v-alert>
            </v-container>
        </v-main>
    </v-app>
</template>
<script>     
export default {
    name: "Approve Experience",
    async mounted(){
        this.$vuetify.theme.dark=false;
    },
    data:() => ({
        user:null,
        empid:null, 
        reason:null,
        dues: null,
        rehire:null,
        searchbox:true,
        relieved :null,
        remarks :null,
        name : null,
        option:['Yes','No'],
        data:null,
        fail:false,
        approve : null,
        reject : null,
        designation:null,
        company : null,
        start_date:null,
        end_date:null,
        reporting_manager:null,
        lpa:null,
    }),
    methods:{
        async fetchdata(){
            let url = "http://127.0.0.1:8000/exp"
            let empiddata = { params :{ 'empid': this.empid}}
            let res = await this.$axios.get(url,empiddata)
            console.log(res.data)
            if (res.data === false){
                this.fail= true
            }
            else{
                this.empid = res.data.empid;
                this.name = res.data.name;
                this.designation = res.data.designation;
                this.company = res.data.company;
                this.start_date = res.data.start_date;
                this.end_date = res.data.end_date;
                this.reporting_manager = res.data.reporting_manager;
                this.lpa= res.data.lpa;
                this.user =true
                this.data= false
                this.searchbox=false
            }
        },
        async update(){
            let url= "http://127.0.0.1:8000/expdataadd";
            let update={
                empid : this.empid,
                rehire: this.rehire,
                reason : this.reason,
                dues : this.dues,
                relieved : this.relieved,
                remarks : this.remarks

            }
            let res = await this.$axios.post(url, update);
            console.log(res.data);
            this.user=false
            this.data=true
        },
        async accept(){
            let url = "http://127.0.0.1:8000/expstatusupdate";
            let empdata= {
                empid : this.empid,
                status : 'approved'
            }
            let res= await this.$axios.post(url, empdata);
            if (res.data == true) {
                this.approve =true;
                this.reject =false;
                this.data=false
            }
        },
        async refuse(){
            let url = "http://127.0.0.1:8000/expstatusupdate";
            let empdata= {
                empid : this.empid,
                status : 'rejected'
            }
            let res= await this.$axios.post(url,empdata);
            if (res.data == true){
                this.reject =true
                this.approve= false
                this.data=false
            }
        },
        async home(){
            this.$router.push('/');
        },
        
    }
}
</script>
<style>
.search{
    width: 20%;
}
</style>