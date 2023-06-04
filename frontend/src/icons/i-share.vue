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
    <svg :height="size" :width="size" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-25.6 -25.6 563.20 563.20" xml:space="preserve" :fill="fill" :stroke="stroke">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="28.672000000000004"> 
            <g> 
                <path class="st0" d="M512,230.431L283.498,44.621v94.807C60.776,141.244-21.842,307.324,4.826,467.379 c48.696-99.493,149.915-138.677,278.672-143.14v92.003L512,230.431z"></path> 
            </g> 
        </g>
        <g id="SVGRepo_iconCarrier"> 
            <g> 
                <path class="st0" d="M512,230.431L283.498,44.621v94.807C60.776,141.244-21.842,307.324,4.826,467.379 c48.696-99.493,149.915-138.677,278.672-143.14v92.003L512,230.431z"></path> 
            </g> 
        </g>
    </svg>
</template>