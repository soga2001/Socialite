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
        <h1>Page Not Found!</h1>
        <RouterLink to="/">Home</RouterLink>
    </div>
</template>

<style scoped>
div {
    text-align: center;
}
div h1 {
    font-size: 100px;
}

a {
    font-size: 30px;
}
</style>