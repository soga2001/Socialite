
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'i_mention',
    props: {
        fill: {
            type: String,
            default: 'var(--color-heading)'
        },
        stroke: {
            type: String,
            default: 'var(--color-background)'
        },
        size: {
            type: String,
            default: '20px',
        },
    }
})
</script>

<template>
    <svg :width="size" :height="size" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" :fill="fill">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        <g id="SVGRepo_iconCarrier">
            <g id="Layer_2" data-name="Layer 2"> 
                <g id="invisible_box" data-name="invisible box"> </g>
                <g id="icons_Q2" data-name="icons Q2"> 
                    <g> 
                        <path d="M24,6A18,18,0,1,1,6,24,18.1,18.1,0,0,1,24,6m0-4A22,22,0,1,0,46,24,21.9,21.9,0,0,0,24,2Z"></path> 
                        <circle cx="14" cy="24" r="4"></circle>
                        <circle cx="24" cy="24" r="4"></circle> 
                        <circle cx="34" cy="24" r="4"></circle> 
                    </g> 
                </g> 
            </g>
        </g>
    </svg>
</template>