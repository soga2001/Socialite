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
        <Item class="item">
            <template #avatar>
              <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
              <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
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



/* .item:hover {
    background-color: red;
    width: fit-content;
    border-radius: 50%;
    padding: 0;
} */
</style>