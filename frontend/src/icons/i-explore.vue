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
    <svg :fill="fill" :height="size" :width="size" viewBox="-3 -3 26.00 26.00" xmlns="http://www.w3.org/2000/svg">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="1">
            <path d="M10 20a10 10 0 1 1 0-20 10 10 0 0 1 0 20zM7.88 7.88l-3.54 7.78 7.78-3.54 3.54-7.78-7.78 3.54zM10 11a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"></path>
        </g>
        <g id="SVGRepo_iconCarrier">
            <path d="M10 20a10 10 0 1 1 0-20 10 10 0 0 1 0 20zM7.88 7.88l-3.54 7.78 7.78-3.54 3.54-7.78-7.78 3.54zM10 11a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"></path>
        </g>
    </svg>
</template>