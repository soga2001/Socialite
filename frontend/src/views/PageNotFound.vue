<script lang="ts">
import { defineComponent } from 'vue';


export default defineComponent({
    data() {
        return {

        }
    }
})
</script>

<template>
    <div class="page__not__found">
        <div>
            <h1>Page Not Found!</h1>
            <RouterLink to="/home">Home</RouterLink>
        </div>
    </div>
</template>

<style scoped>

.page__not__found {
    height: 100vh;
    display: flex;
    justify-content: center;
    justify-items: center;
    align-content: center;
    align-items: center;
}
div {
    text-align: center;
}
div h1 {
    font-size: 70px;
}

a {
    font-size: 30px;
    text-decoration: none;
}
</style>