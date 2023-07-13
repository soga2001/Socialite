<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import type { Notifications } from '@/assets/interfaces';

import TimeagoVue from '@/components/Timeago.vue';
export default defineComponent({
  name: 'notification',
  data() {
    return {
    };
  },
  methods: {

  },
  created() {
    console.log('here')
  },
  mounted() {
  },
  watch: {
  },
});
</script>

<template>
  <div class="w-full">
    <header class="sticky z-4 top-0 border-b bg-blur-2">
      <div v-if="!$q.screen.lt.sm">
        <Item>
          <template #title>
            <span class="text-2xl weight-900">Notifications</span>
          </template>
          <template #icon>
            <q-btn flat round dense icon="settings" size="16px" @click.stop="" />
          </template>
        </Item>
      </div>
      <q-tabs
          class="bg-transparent w-full text-lg text-capitalize"
      >
          <q-route-tab class="text-capitalize" active-class="active" :to="{name: 'all-notif'}" exact replace>
              <span>All</span>
          </q-route-tab>
          <q-route-tab class="text-capitalize" active-class="active"  :to="{name: 'mentions'}" exact replace>
              <span>Mentions</span>
          </q-route-tab>
      </q-tabs>
    </header>
    <div>
      <div class="w-full overflow-hidden min-h-viewport">
        <RouterView v-slot="{ Component }">
            <KeepAlive :max="2" :include="['all-notif', 'mentions']">
                <component :is="Component"/>
            </KeepAlive>
        </RouterView>
      </div> 
    </div>
    
  </div>
</template>

<style scoped lang="scss">

.active {
    span {
        color: var(--color-heading);
        font-weight: 900;
    }
}

span {
    color: var(--color-text);
    font-weight: 800;
}

</style>