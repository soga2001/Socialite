<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import type { Notifications } from '@/assets/interfaces';

import TimeagoVue from '@/components/Timeago.vue';
export default defineComponent({
  name: 'notifications',
  data() {
    return {
      scrollPos: this.scrollPosition || 0,
      scrollHeight: this.scrollHeight || 0,
    };
  },
  props: {
    scrollPosition: {
      type: Number,
      default: 0,
    },
    height: {
      type: Number,
      default: 0,
    },
  },
  methods: {

  },
  created() {
    console.log(this.$parent?.$parent?.$parent?.$route.name)

  },
  mounted() {
    console.log((this.$refs.header as HTMLDivElement)?.offsetLeft)
    console.log((this.$refs.router as HTMLDivElement)?.offsetLeft)
  },
  watch: {

  },
});
</script>

<template>
  <div class="w-full relative">
    <header ref="header" class="sticky top-0 w-full z-5 border-b bg-blur-1">
      <div v-if="!$q.screen.lt.sm" >
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
          ref="tabs"
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
      <!-- :style="{marginTop: `${($refs.header as HTMLDivElement)?.offsetHeight}px`}" -->
      <div ref="router" class="w-full overflow-hidden min-h-viewport">
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