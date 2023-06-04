<template>
    <div class="tooltip">
      <slot></slot>
      <div v-if="showTooltip" class="tooltip-text text-sm weight-900">
        {{ text }}
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  export default defineComponent({
    data() {
      return {
        showTooltip: false
      };
    },
    props: {
      text: {
        type: String,
        required: true
      }
    },
    methods: {
      show() {
        this.showTooltip = true;
      },
      hide() {
        this.showTooltip = false;
      }
    },
    mounted() {
      const tooltipElement = this.$el;
  
      tooltipElement.addEventListener("mouseenter", this.show);
      tooltipElement.addEventListener("mouseleave", this.hide);
    },
    beforeUnmount() {
      const tooltipElement = this.$el;
  
      tooltipElement.removeEventListener("mouseenter", this.show);
      tooltipElement.removeEventListener("mouseleave", this.hide);
    }
  });
  </script>
  
  <style scoped>
  .tooltip {
    position: relative;
    display: inline-block;
  }
  
  .tooltip-text {
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    padding: 8px;
    background-color: var(--color-background-mute);
    color: var(--color-heading);
    border-radius: 4px;
    /* font-size: 14px; */
    opacity: 0;
    transition: opacity 10s ease-in-out;
  }
  
  .tooltip:hover .tooltip-text {
    opacity: 1;
  }
  </style>
  