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
                <img :src="$store.state.user.avatar" alt="John Doe" class="rounded-full" />
            </template>
            <template #name>{{$store.state.user.first_name + ' ' + $store.state.user.last_name}}</template>
            <template #username>{{ $store.state.user.username }}</template>
            <template #icon>
                <img
                src="icon1.png"
                alt="Icon 1"
                @click="() => {}"
                />
                <img
                src="icon2.png"
                alt="Icon 2"
                @click="() => {}"
                />
            </template>
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