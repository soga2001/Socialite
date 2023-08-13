<script lang="ts">
import sidenav from '../components/navbar/sidenav.vue';
export default {
    components: {sidenav},
    data() {
        return {
            user: {},
        }
    },
    mounted() {
        // this.fetchData();
    },
    methods: {
        // async fetchData() {
        //     const res = await $fetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'}).catch((err) => err.data)
        //     console.log('here',(res as {success: boolean, user: []}).user)
        // },
    },
}
</script>

<template>
    <div class="main">
        <aside class="leftbar sticky top-0">
            <sidenav />
        </aside>
        <div class="pages">
            <slot />
        </div>
        <aside class="rightbar sticky top-0">

        </aside>
    </div>
</template>


<style scoped lang="scss">
.main {
    display: grid;
    grid-template-columns: minmax(auto, 400px) 600px 400px;
    height: 100%;
    width: 100%;
    padding: 0;
    margin: 0;
}

.leftbar {
    // background-color: #c22c2c;
    height: 100%;
    width: 100%;
    min-height: 100dvh;
    max-height: 100vh;
}

.pages {
    // background-color: #c22c2c;
    height: 100%;
    width: 100%;
    border-left: 2px solid white;
    border-right: 2px solid white;
}

.rightbar {
    background-color: #c22c2c;
    height: 100%;
    width: 100%;
}
</style>
  