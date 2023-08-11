<template>
    <v-form >
        <v-text-field label="Reason for leaving" v-model="reason"></v-text-field>
        <v-text-field label="Is there any pending dues ?" v-model="dues"></v-text-field>
        <v-text-field label="Is the candidate officially relieved ?" v-model="relieved"></v-text-field> 
        <v-text-field label="Remarks" v-model="remarks"></v-text-field>
        <v-container class="text-center">
            <v-btn text @click="expupdate()" color="blue lighten-1">Update Status</v-btn>
        </v-container>
    </v-form>
</template>
<script>
export default {
    name: "expupdate",
}
</script>