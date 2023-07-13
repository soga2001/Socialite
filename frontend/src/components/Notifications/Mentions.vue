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
    name: "mentions",
    created() {
        this.getNotification();
    },
    methods: {
        async getNotification() {
            this.loading = true;
            http.get(`notifications/mentions/`).then((res) => {
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
    <div v-if="notification.length > 0 && !loading" class="w-full min-h-viewport">
      <div v-for="notif in notification" :key="notif.id" class=" w-full border-b">

        <Item align-items="start" clickable :to="notif.link">
          <template #avatar>
            <img v-if="notif.actor_avatar" :src="notif.actor_avatar" alt="user's avatar"/>
            <i-profile v-else size="4rem" />
          </template>
          <template #title>
            <div class="w-full flex flex-cols gap-1 items-center">
              <div @click.stop="$router.push({name: 'user-profile', params: {username: notif.actor}})">
                  <span class="text-xl pointer hover-underline text-heading weight-900"  >@{{ notif.actor }}</span>
              </div>
              <span>&#183;</span>
              <div>
                  <Timeago class="text-xs text-ligher weight-ligher" :date="notif.timestamp"/>
              </div>
            </div>
          </template>
          <template #caption>
            {{ notif.description }}
          </template>
          <template #icon>
            <q-btn flat round dense icon="more_horiz" size="16px" @click.stop="" />
          </template>
        </Item>
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