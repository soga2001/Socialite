<template>
  <div :class="'user-card ' + (isAvatarOnly ? 'circular' : '')" :style="style" @click="router">
    <div class="avatar" v-if="$slots.avatar">
      <slot name="avatar" />
    </div>
    <div class="info" v-if="!isAvatarOnly">
      <div class="title">
        <slot name="title" v-if="$slots.title" />
      </div>
      <div class="caption">
        <slot name="caption" v-if="$slots.caption" />
      </div>
    </div>
    <div class="icon" :style="style" v-if="!isAvatarOnly">
      <slot name="icon" v-if="$slots.icon" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type {RouteLocationRaw} from 'vue-router'

export default defineComponent({
  data() {
    return {
      isAvatarOnly: true,
      style: {
        alignItems: this.vertIconCenter ? 'center' : 'normal',
        cursor: this.to ? 'pointer' : 'normal'
      }
    };
  },
  props: {
    vertIconCenter: {
      type: Boolean,
      default: false
    },
    to: {
      type: [String, Object] as PropType<RouteLocationRaw>,
      default: null,
    },
    clickable: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    router() {
      if (this.to) {
        this.$router.push(this.to);
      }
    }
  },
  mounted() {
    this.isAvatarOnly = Boolean(
      this.$slots.avatar &&
        !this.$slots.title &&
        !this.$slots.caption &&
        !this.$slots.icon
    );
    console.log(this.$props.clickable)
  }
});
</script>
  
  <style scoped>
  .user-card {
    display: flex;
    /* padding: 0px 0.6rem;
    padding-top: 0.4rem; */
    padding: 0.5rem .5rem;
    cursor: pointer;
    position: relative;
    line-height: normal;
    gap: 10px;
    overflow: hidden;
  }
  
  .user-card.circular {
    width: fit-content;
    padding: 0;
    margin: 0;
  }

  .avatar,
.info,
.icon {
  line-height: 1.2;
}

  .user-card.circular .avatar {
    width: 100%;
    display: inline-flex;
  }
  
  .avatar {
    flex: 0 0 auto;
    max-width: 3rem;
    width: 100%;
    height: 100%;
  }

  :slotted(img) {
    border-radius: 50%;
    width: 100%;
    height: 100%;
    padding: 0 !important;
  }

  .user-card.circular .avatar :slotted(img) {
    border: 2px solid #FF7373;
  }

  
  .info {
    flex: 1 1 auto;
    align-items: center;
  }
  
  .title {
    font-weight: 900;
    font-size: 17px;
    margin-bottom: .4rem;
  }
  
  .icon {
    flex: 0 0 auto;
    display: flex;
    justify-content: center;
    position: relative;
  }


  :slotted(p:deep(a)) {
    font-weight: 900;
    text-decoration: none;
    color: #FF7373;
    
  }

  :slotted(p:deep(a:hover)) {
    text-decoration: underline;
  }

  /* .post__caption:deep(a) {
    font-weight: 900;
    text-decoration: none;
    color: #FE4A4A;
    color: #FF7373;
    color: rgb(250, 89, 164); 
    color: #b16af4;
    color: rgb(37, 192, 114);
    color: rgb(0, 191, 255);
  } */
  </style>
  