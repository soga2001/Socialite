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
    <!-- <svg :fill="fill" :width="size" :height="size" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg" :stroke="stroke">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="1.024"></g>
        <g id="SVGRepo_iconCarrier">
            <title>video</title>
            <path d="M0 26.016q0 2.496 1.76 4.224t4.256 1.76h20q2.464 0 4.224-1.76t1.76-4.224v-20q0-2.496-1.76-4.256t-4.224-1.76h-20q-2.496 0-4.256 1.76t-1.76 4.256v20zM4 26.016v-20q0-0.832 0.576-1.408t1.44-0.608h20q0.8 0 1.408 0.608t0.576 1.408v20q0 0.832-0.576 1.408t-1.408 0.576h-20q-0.832 0-1.44-0.576t-0.576-1.408zM6.016 24h1.984v2.016h2.016v-20h-4v1.984h1.984v2.016h-1.984v1.984h1.984v2.016h-1.984v1.984h1.984v2.016h-1.984v1.984h1.984v2.016h-1.984v1.984zM12 26.016h8v-4h-8v4zM12 20h8v-8h-8v8zM12 10.016h8v-4h-8v4zM22.016 26.016h1.984v-2.016h2.016v-1.984h-2.016v-2.016h2.016v-1.984h-2.016v-2.016h2.016v-1.984h-2.016v-2.016h2.016v-1.984h-2.016v-2.016h2.016v-1.984h-4v20z"></path>
        </g>
    </svg> -->

    <svg :width="size" :height="size" :fill="fill" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" :stroke="stroke">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        <g id="SVGRepo_iconCarrier">
            <path d="M65.3,51.5A14.25,14.25,0,1,0,79.5,65.8,14.32,14.32,0,0,0,65.3,51.5ZM67.8,67a3.09,3.09,0,0,1-1.1-.2l-5.4,5.4a1.71,1.71,0,0,1-1.1.5c-.5,0-.9-.1-1.1-.5a1.82,1.82,0,0,1,0-2.4l5.4-5.4a4.47,4.47,0,0,1,4-5.8,3.09,3.09,0,0,1,1.1.2c.2,0,.2.2.1.4l-2.5,2.4a.37.37,0,0,0,0,.6l1.6,1.6a.48.48,0,0,0,.7,0l2.4-2.4c.1-.1.5-.1.5.1a6.53,6.53,0,0,1,.2,1.1A4.47,4.47,0,0,1,67.8,67Z"></path>
            <circle cx="44.6" cy="36.1" r="16.1"></circle>
            <path d="M48.9,79.7c2.7,0,1.2-1.9,1.2-1.9h0a19.58,19.58,0,0,1-2.5-20.1l.2-.4a1.17,1.17,0,0,0-.9-1.9h0a18.48,18.48,0,0,0-2.4-.1,24.54,24.54,0,0,0-24.2,21c0,1.2.4,3.5,4.2,3.5H48.4A1.75,1.75,0,0,1,48.9,79.7Z"></path>
        </g>
    </svg>


</template>