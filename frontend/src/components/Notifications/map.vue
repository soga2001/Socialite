<script lang="ts">
import { defineComponent } from 'vue';
import type { Notifications } from '@/assets/interfaces';

export default defineComponent({
    props: {
        notification: {
            type: Object as () => Notifications,
            required: true
        }
    },
    data() {
        return {
        };
    },
    computed: {
    },
    methods: {
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
    <q-item class="max-w-viewport w-full" :to="notification.link">
          <q-item-section avatar top >
            <q-avatar size="3.5rem">
              <img :style="{width: '3rem', height: '3rem'}" v-if="notification.actor_avatar" :src="notification.actor_avatar" alt="user's avatar"/>
              <i-profile v-else size="3rem" />
              <q-badge class="absolute bottom-0 right-0 bg-theme" style="border-radius: 50%; width: 25px; height: 25px">
                <q-badge class="absolute-center bg-web-theme" style="border-radius: 50%; width: 20px; height: 20px">
                  <i-mention fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'mention'"/>
                  <i-profile stroke="none" fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'follow'" />
                </q-badge>
              </q-badge>
            </q-avatar>
          </q-item-section>

          <q-item-section top class="flex gap-1">
            <q-item-label lines="1" class="inline-flex gap-1">
              <span @click.stop="$router.push({name: 'user-profile', params: {username: notification.actor}})"  class="text-base pointer hover-underline text-heading weight-900">@{{notification.actor}}</span>
              <span class="text-body"> - </span>
              <span class="text-lighter"><Timeago :date="notification.timestamp"/></span>
            </q-item-label>
            <q-item-label caption lines="1" >
              <span class="text-body">{{ notification.description }}</span>
            </q-item-label>
            <!-- <q-item-label lines="1" class="q-mt-xs text-body2 text-weight-bold text-primary text-uppercase">
              <span class="cursor-pointer">Open in GitHub</span>
            </q-item-label> -->
          </q-item-section>

          <q-item-section top side>
            <q-btn size="12px" flat dense round icon="more_horiz" />
          </q-item-section>
        </q-item>
</template>

<style lang="scss" scoped>

</style>