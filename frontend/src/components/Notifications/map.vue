<script lang="ts">
import { defineComponent } from 'vue';
import type { Notifications } from '@/assets/interfaces';
import convertTime from '@/assets/convertTime';

export default defineComponent({
    props: {
        notification: {
            type: Object as () => Notifications,
            required: true
        }
    },
    data() {
        return {
            date_posted: convertTime(this.notification.timestamp, 'short'),
            toolTipDate: convertTime(this.notification.timestamp, 'absolute'),

        };
    },
    computed: {
    },
    methods: {
        alert() {
        }
    },
    created() {
    },
    mounted() {
    },
    watch: {
    },
    components: {}
})
</script>

<template>

    <Item class="max-w-viewport w-full pointer" clickable align-items="start" :to="notification.link" avatarSize="3.5rem">
        <template #avatar>
            
            <q-avatar>
                <img :style="{width: '3rem', height: '3rem'}" v-if="notification.actor_avatar" :src="notification.actor_avatar" alt="user's avatar"/>
                <i-profile v-else size="3rem" />
                <q-badge class="absolute bottom-0 right-0 bg-theme" style="border-radius: 50%; width: 25px; height: 25px">
                <q-badge class="absolute-center bg-web-theme" style="border-radius: 50%; width: 20px; height: 20px">
                    <i-mention fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'mention'"/>
                    <i-profile stroke="none" fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'follow'" />
                </q-badge>
                </q-badge>
            </q-avatar>
        </template>
        <template #title>
            <span class="w-full flex flex-cols gap-1 items-center">
                <div>
                    <span class="text-base pointer hover-underline text-heading weight-900"  @click.stop="$router.push({name: 'user-profile', params: {username: notification.actor}})">@{{ notification.actor }}</span>
                </div>
                <span>&#183;</span>
                <div>
                    <span class="text-body text-base">
                        {{ date_posted }}
                        <q-tooltip class="bg-theme box-shadow">
                            <div class="text-body text-sm" v-html="toolTipDate"></div>
                        </q-tooltip>
                    </span>
                </div>
            </span>
        </template>
        <template #caption>
            <span class="text-body">{{ notification.description }}</span>
        </template>
        <template #icon>
            <q-btn @click.stop="alert" size="12px" flat dense round icon="more_horiz" />
        </template>
    </Item>
</template>

<style lang="scss" scoped>

</style>