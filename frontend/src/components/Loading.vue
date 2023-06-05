<script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    props: {
      size: {
        type: String,
        default: '3rem',
        validator:  (value: String) :boolean => /^[0-9]+(px|em|rem|vh|vw|%)$/.test(value.toString()),
      },
      color: {
        type: String,
        default: '#FF7373',
        validator: (value: string): boolean => /^#([0-9A-Fa-f]{3}){1,2}$/.test(value),
      },
      alpha: {
        type: Number,
        default: .3,
        validator: (value: number): boolean => value >= 0 && value <= .5,
      },
      strokeWidth: {
        type: Number,
        default: 3,
        validator: (value: number): boolean => value >= 0,
      }
    },
    data() {
        return {
            defaultSize: '3rem',
            borderColor: this.hex2rgba(this.color, this.alpha)
        }
    },
    methods: {
        hex2rgba(color: string, alpha: number) {
            const [r, g, b] = color?.match(/\w\w/g)!.map((x: string) => parseInt(x, 16));
            const result = `${this.strokeWidth}px solid rgba(${r},${g},${b},${alpha})`
            return result;
        },
    },
    created() {
    },
    mounted() {
    }
  });
</script>

<template>
  <div class="">
    <div class="flex w-full justify-center items-center flex-col gap-2">
      <div id="spinner" class="spinner" :style="{ width: size, height: size, border: borderColor, borderTopColor: color}"></div>
    </div>
    <div class="text-2xl weight-900">
      <slot name="text"></slot>
    </div>
  </div>
  
  
  
</template>
  
  <style scoped>
 .spinner {
    color: rgb(255, 115, 115);
    border-radius: 50%;
    width: 0;
    height: 0;
    animation: spinner .75s linear infinite;
}
  
  @keyframes spinner {
    to { transform: rotate(360deg); }
  }
  </style>
  