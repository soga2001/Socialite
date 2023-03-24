<template>
  <div :class="'user-card ' + (isAvatarOnly ? 'circular' : '')">
    <div class="avatar" v-if="$slots.avatar">
      <slot name="avatar"  />
    </div>
    <div class="info" v-if="!isAvatarOnly">
      <div class="title">
        <slot name="title" v-if="$slots.title" />
      </div>
      <div class="caption">
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

    },
    mounted() {
      this.isAvatarOnly =  Boolean(this.$slots.avatar && !this.$slots.title && !this.$slots.caption && !this.$slots.icon);
    }
  });
  </script>
  
  <style scoped>
  .user-card {
    display: flex;
    /* align-items: center; */
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

  .user-card.circular .avatar {
    width: 100%;
    display: inline-flex;
  }
  
  .avatar {
    flex: 0 0 auto;
    width: 4rem;

  }

  :slotted(img) {
    border-radius: 50%;
    max-width: 50px;
    max-height: 50px;
    padding: 0 !important;
  }

  .user-card.circular .avatar :slotted(img) {
    border: 2px solid #FF7373;
  }

  
  .info {
    flex: 1 1 auto;
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


  :slotted(p:deep(a)) {
    font-weight: 900;
    text-decoration: none;
    color: #FF7373;
    
  }

  :slotted(p:deep(a:hover)) {
    text-decoration: none;
    color: rgb(0, 191, 255);
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
  