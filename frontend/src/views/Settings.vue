<script lang="ts">
import { defineComponent, ref } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Item from '../components/Item.vue'

// import imageCropper from '@/components/imageCropper.vue';

export default defineComponent({
    props: {
        height: {
            type: Number,
            default: 0
        },
        scrollPosition: {
            type: Number,
            default: 0
        },
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
    <div class="relative w-full">
        <div class="banner">

        </div>
        <div class="avatar">

        </div>
        <div>
            Hello
        </div>
    </div>
</template>

<style scoped lang="scss">

/* HSL */
$color1: hsla(117%, 50%, 84%, 1);
$color2: hsla(114%, 15%, 75%, 1);
$color3: hsla(305%, 12%, 61%, 1);
$color4: hsla(327%, 19%, 45%, 1);
$color5: hsla(319%, 13%, 5%, 1);


code {
  padding: 5px 0px;
}

.banner {
    background: $color2;
    width: 100%;
    aspect-ratio: 3/1;
}

.avatar {
    background: $color3;
    height: 150px;
    width: 150px;
    border-radius: 50%;
    margin-left: 20px;
    position: relative;
    top: -75px;
    border: 5px solid $color5;
}
</style>