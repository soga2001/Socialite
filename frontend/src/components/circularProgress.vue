<script lang="ts">
import { defineComponent, type CSSProperties } from 'vue';

export default defineComponent({
    data() {
        return {
        }
    },
    props: {
        maxVal: {
            type: Number,
            default: 255,
        },
        minVal: {
            type: Number,
            default: 0,
        },
        val: {
            type: Number,
            required: true
        },
        size: {
            type: String,
            default: '50px'
        },
    },
    methods: {
        changeStyle(): CSSProperties {
            return {
                background: `radial-gradient(closest-side, var(--color-background) 80%, transparent 80% 100%), conic-gradient(rgb(255, 105, 180) ${(this.val / this.maxVal)*100}%, rgba(255, 192, 203) 0%)`,
                width: this.size,
                height: this.size
            }
        }
    },
    watch: {
        val(value) {
        }
    },
    created() {
        // console.log((this.maxVal + this.val)/this.maxVal)
    },
})
</script>

<template>
    <!-- <div class="progress-bar" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div> -->
    <div class="progress-bar" :style="changeStyle()" role="progressbar" :aria-valuenow="val" :aria-valuemin="minVal" :aria-valuemax="maxVal">
    </div>
</template>

<style scoped>
.progress-bar {
  width: 100px;
  height: 100px;
  border-radius: 50%; 
}
</style>