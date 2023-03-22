<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Item from '../components/Item.vue'
import Cropper from '@/components/Cropper.vue';

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
    },
    components: { Item, Cropper }
})
</script>

<template>
    <div>
        <Item>
            <template #avatar>
                <img src="http://www.gravatar.com/avatar/{{$cookies.gravatar}}?s=50" class="avatar" />
            </template>
            <template #title>
                <h1>Hello</h1>
            </template>
            <!-- <template #subtitle>
                <p>World</p>
            </template> -->
            <!-- <template #actions>
                <RouterLink to="/">Here</RouterLink>
            </template> -->
        </Item>
        <!-- <Cropper /> -->
    </div>
</template>

<style scoped>
/* div {
    min-height: 100vh;
    height: 100%;
} */
</style>