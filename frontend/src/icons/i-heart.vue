<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'o_like',
    props: {
        fill: {
            type: String,
            default: "red"
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
    <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" :width="size" :height="size" viewBox="-5.76 -5.76 75.52 75.52" enable-background="new 0 0 64 64" xml:space="preserve" stroke="white">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="2"></g>
        <g id="SVGRepo_iconCarrier">
            <path :fill="fill" d="M48,5c-4.418,0-8.418,1.791-11.313,4.687l-3.979,3.961c-0.391,0.391-1.023,0.391-1.414,0 c0,0-3.971-3.97-3.979-3.961C24.418,6.791,20.418,5,16,5C7.163,5,0,12.163,0,21c0,3.338,1.024,6.436,2.773,9 c0,0,0.734,1.164,1.602,2.031s24.797,24.797,24.797,24.797C29.953,57.609,30.977,58,32,58s2.047-0.391,2.828-1.172 c0,0,23.93-23.93,24.797-24.797S61.227,30,61.227,30C62.976,27.436,64,24.338,64,21C64,12.163,56.837,5,48,5z M57,22 c-0.553,0-1-0.447-1-1c0-4.418-3.582-8-8-8c-0.553,0-1-0.447-1-1s0.447-1,1-1c5.522,0,10,4.478,10,10C58,21.553,57.553,22,57,22z"></path>
        </g>
    </svg>
</template>