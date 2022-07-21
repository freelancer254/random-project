<template>
    <div class="about">
        <Fieldset legend="About" :toggleable="true">
            <p>{{about}}</p>
        </Fieldset>
    <hr>
    <div class="getStarted">
    <Button @click="getDocs" label="Try The Random Project REST API Now" icon="pi pi-code" class="font-bold px-5 py-3 p-button-raised p-button-rounded white-space-nowrap"></Button>
    </div>
    </div>

</template>

<script>
export default {
    data() {
        return {
            about : null,
        }
    },
    mounted() {
         fetch('https://wby808.deta.dev/about/')
        .then((response) => { return response.json()})
        .then((jsonData) => { this.about = jsonData.data.about});
    },
    methods:{
        getDocs (){
            window.open("https://wby808.deta.dev/docs","_blank")
        }
    }
    
}
</script>

<style scoped>
.about {
    margin: 10px 0;
}
.getStarted {
display: flex;
justify-content: center;
}

</style>