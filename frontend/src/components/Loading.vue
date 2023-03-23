<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    
})
</script>

<template>
    <main>
        <q-spinner  size="3em"/>
        <h1 class="title">Loading...</h1>
    </main>
</template>

<style scoped>
main {
    width: 100%;
    height: 100vh;
    height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: #FF7373;
    font-size: 40px;
}

.title {
    color: var(--color-heading);
    font-size: 50px;
}
</style>