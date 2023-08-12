<script lang="ts">
import sidenav from '../components/navbar/sidenav.vue';
export default {
    components: {sidenav}
}
</script>

<template>
    <div class="main">
        <div class="leftbar">
            <sidenav />
        </div>
        <div class="pages">
            <slot />
        </div>
        <div class="rightbar">

        </div>
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
    background-color: #c22c2c;
    height: 100%;
    width: 100%;
    min-height: 100dvh;
    max-height: 100vh;
}

.rightbar {
    background-color: #c22c2c;
    height: 100%;
    width: 100%;
}
</style>
  