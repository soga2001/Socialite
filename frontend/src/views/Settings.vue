<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'

export default defineComponent({
    data() {
        return {
            
        }
    },
    setup() {
        const store = useStore()
        const {cookies} = useCookies();
        return {cookies};
    },
    methods: {
        
    },
    created() {
        // console.log(import.meta.env)
        // console.log(window.innerHeight)
    }
})
</script>

<template>
    <div>
        
    </div>
</template>

<style scoped>
div {
    min-height: 100vh;
    height: 100%;
}
</style>