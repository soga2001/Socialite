<script lang="ts">
import {defineComponent} from 'vue';


import { http } from '@/assets/http';
import type {Notifications} from '@/assets/interfaces'
import Map from './map.vue'


export default defineComponent({
    data() {
        return {
            notification: new Array<Notifications>(),
            loading: true,

            hasMore: true,
            page: 0,
            userTimeStamp: new Date()
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
          await http.get(`notifications/mentions/`, {
            params: {
              page: this.page,
              userTimeStamp: this.userTimeStamp
            }
          }).then((res) => {
            if(res.data.notifications) {
              if((res.data.notifications).length < 20) {
                this.hasMore = false
              }
              this.notification = [...this.notification, ...res.data.notifications];
            }
            else {
              this.hasMore = false
            }
          }).catch((err) => {
            this.hasMore = false
          });
          this.loading = false;
        }
    },
    components: {Map},
});
</script>

<template>
    <div v-if="notification.length > 0 && !loading" class="w-full min-h-viewport">
      <div v-for="notif in notification" :key="notif.id" class=" w-full border-b">

        <Map :notification="notif" />
      </div>
    </div>
    <div v-else-if="loading" class="pt-3">
      <Loading :stroke-width="5"/>
    </div>
    <div v-else>
      <div class="w-full">
        <div class="w-full flex flex-col gap-1 items-center">
          <i-folder/>
          <div class="text-xl weight-900 text-center">When you have notifications, it will appear here.</div>
        </div>
      </div>
    </div>
</template>

<script lang="scss" scoped>

</script>