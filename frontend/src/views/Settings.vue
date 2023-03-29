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
        },
        check_cookie() {
            http.get('users/check_cookies/').then((res) => {
                console.log(res.data)
            }).catch((err) => {
                console.log(err)
            })
        },
        get_session() {
            http.get('users/get_session').then((res) => {
                console.log(res.data)
                }).catch((err) => {
                    console.log(err)
            })
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
        <Item class="item" :caption-line-clamp="2" align-items="flex-start">
            <template #avatar>
              <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
              <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
            </template>
            <template #title>
                Lorem ipsum dolor sit amet,
            </template>
            <template #caption>
                <p>Lorem ipsum dolor sit amet, consectetur  </p>
            </template>
            <template #icon>
                <q-btn size="10px" flat rounded icon="o_more_horiz"/>
            </template>
        </Item>
        <!-- <Cropper /> -->
        <!-- <button @click="check_cookie">Btn</button>
        <button @click="get_session"> BTN 2</button> -->
    </div>
</template>

<style scoped>
</style>