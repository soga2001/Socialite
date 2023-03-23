<template>
  <div :class="'user-card ' + (isAvatarOnly ? 'circular' : '')">
    <div class="avatar" v-if="$slots.avatar" :style="avatarStyle">
      <slot name="avatar"  />
    </div>
    <div class="info" v-if="!isAvatarOnly">
      <div class="title">
        <slot name="title" v-if="$slots.title" />
      </div>
      <div class="sub-title">
        <slot name="caption" v-if="$slots.caption" />
      </div>
    </div>
    <div class="icon" v-if="!isAvatarOnly">
      <slot name="icon" v-if="$slots.icon" />
    </div>
  </div>
</template>
  
<script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    data() {
      return {
        isAvatarOnly: true
      };
    },
    computed: {
      avatarStyle() {
        if (this.isAvatarOnly) {
          return {
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '50%'
          };
        }
        return {};
      }
    },
    mounted() {
      this.isAvatarOnly =  Boolean(this.$slots.avatar && !this.$slots.title && !this.$slots.caption && !this.$slots.icon);
    }
  });
  </script>
  
  <style scoped>
  .user-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem;
    cursor: pointer;
    position: relative;
  }
  
  .user-card.circular {
    width: fit-content;
    padding: 0;
    margin: 0;
  }
  
  .avatar {
    flex: 0 0 auto;
    width: 3rem;
  }
  
  .info {
    flex: 1 1 auto;
    margin-left: .5rem;
  }
  
  .title {
    font-weight: 900;
    font-size: 17px;
  }
  
  .icon {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    position: relative;
  }
  
  :slotted(img) {
    border-radius: 50%;
    max-width: 50px;
    max-height: 50px;
    padding: 0 !important;
  }

  :slotted(*):deep() {
    padding: 10px;
  }
  </style>
  