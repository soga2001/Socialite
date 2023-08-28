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
    console.log('tomato')

  },
  mounted() {
    console.log('potato')
  },
  watch: {

  },
});
</script>

<template>
  <div class="w-full relative">
    <div >
      <div ref="router" :class="{'min-h-viewport': !$q.screen.lt.sm}" class="w-full overflow-hidden ">
        <RouterView v-slot="{ Component }">
            <KeepAlive :include="['all-notif', 'mentions']">
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