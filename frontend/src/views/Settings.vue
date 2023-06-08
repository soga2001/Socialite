<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Item from '../components/Item.vue'

// import imageCropper from '@/components/imageCropper.vue';

export default defineComponent({
    props: {
        
    },
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
    },
    components: { Item }
})
</script>

<template>
</template>

<style scoped>
</style>