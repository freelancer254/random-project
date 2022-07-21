<script>
export default {
    data(){
        return{
            menuitems:[
                {
                   label:'A Random Project',
                   icon:'pi pi-fw pi-code',
                   url:"#"
                },
                {
                    label: 'Documentation',
                    icon: 'pi pi-fw pi-file',
                    url:"https://wby808.deta.dev/docs",
                    target : "blank"
                },
                 {
                    label: 'Github',
                    icon: 'pi pi-fw pi-github',
                    url:"https://github.com/freelancer254",
                    target: "blank"
                },
                 {
                    label: 'Buy Me A Coffee',
                    icon: 'pi pi-fw pi-heart-fill',
                    url:"https://www.buymeacoffee.com/freelancer254",
                    target: "blank"
                },
            ]
        }
    }
}
</script>

<template>
    <TabMenu :model="menuitems"></TabMenu>
</template>

<style scoped>

</style>