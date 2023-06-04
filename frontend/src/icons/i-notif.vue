<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'i_explore',
    props: {
        fill: {
            type: String,
            default: 'var(--color-background)'
        },
        stroke: {
            type: String,
            default: 'var(--color-heading)'
        },
        size: {
            type: String,
            default: '20px',
        },
    }
})
</script>

<template>
    <svg :fill="fill" :width="size" :height="size" viewBox="0 0 24.00 24.00" xmlns="http://www.w3.org/2000/svg">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="1.206">
            <path d="M10,20h4a2,2,0,0,1-4,0Zm8-4V10a6,6,0,0,0-5-5.91V3a1,1,0,0,0-2,0V4.09A6,6,0,0,0,6,10v6L4,18H20Z"></path>
        </g>
        <g id="SVGRepo_iconCarrier">
            <path d="M10,20h4a2,2,0,0,1-4,0Zm8-4V10a6,6,0,0,0-5-5.91V3a1,1,0,0,0-2,0V4.09A6,6,0,0,0,6,10v6L4,18H20Z"></path>
        </g>
    </svg>
</template>