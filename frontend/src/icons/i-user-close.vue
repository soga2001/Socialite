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

    <svg :width="size" :height="size" viewBox="-2.4 -2.4 28.80 28.80" fill="none" xmlns="http://www.w3.org/2000/svg" :stroke="stroke">
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        <g id="SVGRepo_iconCarrier"> 
            <path :fill="fill" fill-rule="evenodd" clip-rule="evenodd" d="M16.5 7.063C16.5 10.258 14.57 13 12 13c-2.572 0-4.5-2.742-4.5-5.938C7.5 3.868 9.16 2 12 2s4.5 1.867 4.5 5.063zM4.102 20.142C4.487 20.6 6.145 22 12 22c5.855 0 7.512-1.4 7.898-1.857a.416.416 0 0 0 .09-.317C19.9 18.944 19.106 15 12 15s-7.9 3.944-7.989 4.826a.416.416 0 0 0 .091.317z"></path>
            <!-- <path d="M12.17157 17.82844C12.56209 18.21896 13.1953 18.21896 13.58582 17.82844L15 16.41423L16.41423 17.82844C16.80475 18.21896 17.43792 18.21896 17.82844 17.82844C18.21896 17.43792 18.21896 16.80475 17.82844 16.41423L16.41423 15L17.82844 13.58577C18.21896 13.19525 18.21896 12.56208 17.82844 12.17156C17.43792 11.78103 16.80475 11.78103 16.41423 12.17156L15 13.58577L13.58582 12.17156C13.1953 11.78103 12.56209 11.78103 12.17157 12.17156C11.78104 12.56208 11.78104 13.19525 12.17157 13.58577L13.58582 15L12.17157 16.41423C11.78104 16.80475 11.78104 17.43792 12.17157 17.82844Z" fill="#e0e3eb"/> -->
            <g id="SVGRepo_iconCarrier" >
                <path d="M15 16L20 21M20 16L15 21M11" stroke="red" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></path>
            </g>
        </g>
    </svg>
    
    <!-- <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        
    </svg> -->

</template>