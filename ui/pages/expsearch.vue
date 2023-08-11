<template>
    <v-app expsearch>
        <v-container class="text-center" fluid style="width:30%">
            <v-text-field label="Enter Employee ID" v-model="empid"></v-text-field>
            <v-btn text @click="search()" color="blue lighten-1" width="200px">Search</v-btn><br/><br/>
        </v-container>
            <v-container v-if="exit" fluid style="width:30%">
                <v-card>
                  <v-card-title> Employee ID :{{ employee.empid }}</v-card-title>
                    <v-container>
                        Name : {{ employee.name }} <br/>
                        Designation : {{ employee.designation}}<br/>
                        Start Date : {{ employee.start_date }}<br/>
                        End Date : {{ employee.end_date }}<br/>
                        Reporting Manager : {{ employee.reporting_manager}} <br/>
                        CTC : {{ employee.lpa}} <br/>
                    </v-container>
                  <v-card-actions>
                </v-card-actions>
                </v-card>
            </v-container>
    </v-app>
</template>
<script>
export default{
    name:"expsearch",
    layout:'profileform_layout',
    async mounted(){
        this.$vuetify.theme.dark=false;
    },
    data:() =>({
        empid:"",
        employee: {},
        exit: null,
    }),
    methods:{
        async search(){
            let url = "http://127.0.0.1:8000/exp"
            let empiddata = { params :{ 'empid': this.empid}}
            let res = await this.$axios.get(url,empiddata)
            this.exit= true
            this.employee = res.data
            console.log(res.data)
        },
    }
}
</script>