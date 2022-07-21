
<template>
<Header/>
<About/>
<RandomRequests/>
</template>

<script>
import Header from "./components/Header.vue"
import About from "./components/About.vue"
import RandomRequests from "./components/RandomRequests.vue"

export default {
  name: "app",
  components:{
    Header,
    About,
    RandomRequests,
  }
}
</script>

<style scoped>

</style>
