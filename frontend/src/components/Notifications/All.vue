<script lang="ts">
import {defineComponent} from 'vue';


import { http } from '@/assets/http';
import type {Notifications} from '@/assets/interfaces'


export default defineComponent({
    data() {
        return {
            notification: new Array<Notifications>(),
            loading: true,
        };
    },
    props: {},
    name: "all",
    created() {
        this.getNotification();
    },
    methods: {
        async getNotification() {
            this.loading = true;
            http.get(`notifications/all/`).then((res) => {
              console.log(res.data)
              this.notification = [...this.notification, ...res.data.notifications];
            }).catch((err) => {
                console.log(err);
            });
            setTimeout(() => {
                this.loading = false;
            }, 3000);
            // this.loading = false;
        }
    },
});
</script>

<template>
    <div v-if="notification.length > 0 && !loading" class="w-full max-w-viewport overflow-x-hidden min-h-viewport">
      <div v-for="notif in notification" :key="notif.id" class="w-full max-w-viewport border-b">
        <q-item class="max-w-viewport w-full" :to="notif.link">
          <q-item-section avatar top class="relative">
            <q-avatar size="4rem">
              <img v-if="notif.actor_avatar" :src="notif.actor_avatar" alt="user's avatar"/>
              <i-profile v-else size="4rem" />
              <q-badge color="white" class="absolute-bottom-right" style="border-radius: 10px; width: 22px; height: 22px">
                <q-badge class="absolute-center bg-transparent" style="border-radius: 7px; width: 20px; height: 20px">
                  <i-mention :style="{transform: 'scale(2)'}" class="bg-transparent" v-if="notif.verb == 'mention'"/>
                  <i-profile :style="{transform: 'scale(2)'}" v-if="notif.verb == 'follow'" />
                </q-badge>
              </q-badge>
            </q-avatar>
          </q-item-section>

          <q-item-section top>
            <q-item-label lines="1" class="inline-flex gap-1">
              <span @click.stop="$router.push({name: 'user-profile', params: {username: notif.actor}})"  class="text-base pointer hover-underline text-heading weight-900">@{{notif.actor}}</span>
              <span class="text-body"> - </span>
              <span class="text-body"><Timeago :date="notif.timestamp"/></span>
            </q-item-label>
            <q-item-label caption lines="1">
              {{ notif.description }}
            </q-item-label>
            <!-- <q-item-label lines="1" class="q-mt-xs text-body2 text-weight-bold text-primary text-uppercase">
              <span class="cursor-pointer">Open in GitHub</span>
            </q-item-label> -->
          </q-item-section>

          <q-item-section top side>
            <q-btn size="12px" flat dense round icon="more_horiz" />
          </q-item-section>
        </q-item>
      </div>
    </div>
    <div v-else-if="loading" class="pt-3">
      <Loading :stroke-width="5"/>
    </div>
    <div v-else>
      <div class="w-full">
        <div class="w-full flex flex-col gap-1 items-center">
          <i-folder/>
          <div class="text-3xl text-center text-heading weight-900">When you have notifications, it will appear here.</div>
        </div>
      </div>
    </div>
</template>

<script lang="scss" scoped>

</script>