<script lang="ts">
import { defineComponent } from 'vue';

import type { Notifications } from '@/assets/interfaces';
import Item from '../Item.vue';
import iProfileVue from '@/icons/i-profile.vue';
import IMention from '@/icons/i-mention.vue';

export default defineComponent({
    name: 'notification-toast',
    data() {
        return {

        };
    },
    props: {
        notification: {
            type: Object as () => Notifications,
            required: true,
        },
    },
    methods: {
        clicked() {
            // console.log('here')
            console.log(this.notification.link)
        },
    },
    mounted() {
    },
    created() {
    },
    computed: {
    },
    watch: {
    },
    components: {
    Item,
    iProfileVue,
    IMention
},
})
</script>

<template>
    <div class="bg-transparent h-full w-full" @click.stop="clicked">
        <Item class="w-full bg-theme box-shadow mb-2" clickable :to="`/${notification.link}`">
            <template #avatar>
                <q-avatar>
                    <img height="3rem" width="3rem" v-if="notification.actor_avatar" :src="notification.actor_avatar" alt="user's avatar"/>
                    <iProfileVue v-else size="3rem" />
                    <q-badge class="absolute bottom-0 right-0 bg-theme" style="border-radius: 50%; width: 25px; height: 25px">
                        <q-badge class="absolute-center bg-web-theme" style="border-radius: 50%; width: 20px; height: 20px">
                            <IMention fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'mention'" />
                            <iProfileVue stroke="none" fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'follow'" />
                        </q-badge>
                    </q-badge>
                </q-avatar>
            </template>
            <template #title>
                <div class="text-xl weight-900">@{{ notification.actor }}</div>
            </template>
            <template #caption>
                <div class="text-base weight-500 text-body">{{ notification.description }}</div>
            </template>
        </Item>
    </div>

</template>


<style scoped lang="scss">


</style>