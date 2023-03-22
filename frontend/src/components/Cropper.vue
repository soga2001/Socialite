<script lang="ts">
import { defineComponent } from 'vue';


export default  defineComponent({
    name: 'Cropper',
    data() {
        return {
            img: "https://images.unsplash.com/photo-1600984575359-310ae7b6bdf2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=80"
        }
    },
    methods: {
        change({coordinates, canvas}: {coordinates: { x: number, y: number, width: number, height: number }, canvas: HTMLCanvasElement }) {
            // Function body
            console.log('here')
        }
    },
    mounted() {
        console.log('here')
    }
})

</script>

<template>
<!-- <cropper
	class="cropper"
	:src="img"
	:stencil-props="{
		aspectRatio: 10/12
	}"
	@change="change"
/> -->
<!-- <cropper
	src="https://images.pexels.com/photos/1254140/pexels-photo-1254140.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
  /> -->
</template>

<style scoped>
.cropper {
	height: 600px;
	width: 600px;
	background: #DDD;
}
</style>