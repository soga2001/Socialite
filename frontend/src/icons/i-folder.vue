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
    <svg height="200px" width="200px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 226.512 226.512" xml:space="preserve" :fill="fill" :stroke="stroke">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" :stroke="stroke" stroke-width="1.812096"></g>
        <g id="SVGRepo_iconCarrier"> 
            <g> 
                <path style="fill:#ffffff;" d="M186.268,9.011H38.929c0,0-3.04,0-6.799,0c-3.753,0-8.577,4.536-10.764,10.128L3.009,65.958 c-2.187,5.591-3.47,14.974-2.856,20.951l12.287,119.774c0.609,5.978,5.983,10.818,11.988,10.818h177.672 c6.005,0,11.379-4.846,11.988-10.818l12.287-119.774c0.609-5.978-0.87-15.273-3.312-20.755l-21.414-47.238 C199.158,13.444,192.272,9.011,186.268,9.011z M148.162,148.615H78.362c-6.005,0-10.878-4.873-10.878-10.878v-24.476 c0-6.005,4.873-10.878,10.878-10.878h69.799c6.005,0,10.878,4.873,10.878,10.878v24.476 C159.04,143.742,154.166,148.615,148.162,148.615z M28.834,68.514l6.88-20.201c1.936-5.684,8.376-10.296,14.386-10.296h122.896 c6.005,0,12.863,4.444,15.311,9.932l9.361,20.935c2.448,5.488-0.435,9.932-6.445,9.932H36.209 C30.199,78.816,26.898,74.204,28.834,68.514z"></path> 
            </g> 
        </g>
    </svg>
</template>