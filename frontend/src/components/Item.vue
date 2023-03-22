<template>
    <div class="user-card">
      <div class="avatar">
        <slot name="avatar" />
      </div>
      <div class="info">
        <div class="title">
          <slot name="title" />
        </div>
        <div class="sub-title">
          <slot name="sub-title" />
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
    padding: .6rem;
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
  
  .title {
    font-weight: 900;
    font-size: 17px;
    margin-bottom: 0.3rem;
  }
  
  .sub-title {
    font-style: italic;
  }
  
  .icon {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
  }
  </style>
  