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
        handleItemClick() {
            console.log('clicked')
        }
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
            <template #title>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </template>
            <template #caption>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            </template>
            <template #icon>
                <q-icon name="o_more_horiz"/>
            </template>
        </Item>
        <!-- <Cropper /> -->
    </div>
</template>

<style scoped>
div {
    max-width: 100%;
}
.item {
    height: fit-content;
    /* background-color: lightblue; */
}
</style>