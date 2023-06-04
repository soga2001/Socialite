<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'o_home',
    props: {
        fill: {
            type: String,
            default: 'var(--color-heading)'
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
    <svg :fill="fill" :width="size" :height="size" viewBox="-3.2 -3.2 38.40 38.40" version="1.1" xmlns="http://www.w3.org/2000/svg" :stroke="stroke" stroke-width="0.00032" transform="rotate(0)">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="1.984"> 
            <title>home</title> 
            <path d="M0 14.016l2.016 1.984h4v14.016q0 0.832 0.576 1.408t1.408 0.576h4v-8q0-0.832 0.576-1.408t1.44-0.576h4q0.8 0 1.408 0.576t0.576 1.408v8h4q0.832 0 1.408-0.576t0.608-1.408v-14.016h4l1.984-1.984-16-14.016zM12 14.016q0-1.664 1.184-2.848t2.816-1.152 2.816 1.152 1.184 2.848-1.184 2.816-2.816 1.184-2.816-1.184-1.184-2.816z"></path> 
        </g>
        <g id="SVGRepo_iconCarrier"> 
            <title>home</title> 
            <path d="M0 14.016l2.016 1.984h4v14.016q0 0.832 0.576 1.408t1.408 0.576h4v-8q0-0.832 0.576-1.408t1.44-0.576h4q0.8 0 1.408 0.576t0.576 1.408v8h4q0.832 0 1.408-0.576t0.608-1.408v-14.016h4l1.984-1.984-16-14.016zM12 14.016q0-1.664 1.184-2.848t2.816-1.152 2.816 1.152 1.184 2.848-1.184 2.816-2.816 1.184-2.816-1.184-1.184-2.816z"></path> 
        </g>
    </svg>
</template>