<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    name: 'uploadedImg',
    props: {
        imgUrl: {
            type: String,
            required: true
        }
    },
    data() {
        return {
        }
    },
    methods: {
        onDelete() {
            this.$emit('update:delete')
        }
    },
})
</script>

<template>
    <div class="container rounded">
        <img :src="imgUrl" alt="Snow" class="w-full rounded">
        <!-- <button @click="onDelete" class="top-right border-none btn bg-transparent text-2xl">X</button> -->
        <i-close @click="onDelete" fill="black" stroke="white" size="2.5rem" class="top-right" />
    </div>
</template>

<style scoped>
.container {
  position: relative;
  text-align: center;
  color: black;
}

.top-right {
  position: absolute;
  top: 8px;
  right: 16px;
}
</style>