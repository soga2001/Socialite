<template>
    <div class="user-card">
      <div class="avatar">
        <slot name="avatar" />
      </div>
      <div class="info">
        <div class="name">
          <slot name="name" />
        </div>
        <div class="username">
          <slot name="username" />
        </div>
      </div>
      <div class="icon">
        <slot name="icon" />
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    data() {
      return {};
    },
  });
  </script>
  
  <style scoped>
  .user-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border: 1px solid #ccc;
    /* border-radius: 0.5rem; */
    cursor: pointer;
  }
  
  .avatar {
    flex: 0 0 auto;
    margin-right: 1rem;
    width: 3rem;
  }

:slotted(img) {
    border-radius: 50%;
    max-width: 50px;
    max-height: 50px;
}


  
  .info {
    flex: 1 1 auto;
  }
  
  .name {
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .username {
    font-style: italic;
  }
  
  .icon {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
  }
  </style>
  