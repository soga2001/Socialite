<script lang="ts">
import { defineComponent, type CSSProperties } from 'vue';
import type { AspectRatio } from 'vue-advanced-cropper';

export default defineComponent({
    name: 'ZoomImg',
    props: {
        img: {
            type: String,
            required: true,
        },
        open: {
            type: Boolean,
            required: true,
        }
    },
    data() {
        return {
            image: new Image(),
            imgHeight: 0,
            imgWidth: 0,
            aspectRatio: 1,

        }
    },
    created() {
        
    },
    mounted() {
        this.image.src = this.img
        this.imgHeight = this.image.height
        this.imgWidth = this.image.width
    },
    methods: {
        close() {
            this.$emit('update:open', false)
        }

    },
    watch: {
        imgHeight(imgHeight) {
            console.log('height',imgHeight)
        },
        imgWidth(imgWidth) {
            this.aspectRatio = imgWidth / this.imgHeight
            console.log('width',this.aspectRatio)
        }
    },

});
</script>

<template>
   <q-dialog v-model="open" :maximized="true">
      <q-card :style="{backgroundColor: 'rgba(0,0,0,.9)'}" class="w-full h-full p-0 m-0" @click="close">
        <q-card-section class="h-full flex justify-center items-center relative">
          <q-btn class="absolute top-0 right-0 m-2 z-3 p-1"  flat round dense>
            <q-icon name="close" color="white" size="2.5rem" />
          </q-btn>
          <q-img :class="{'aspectRatio-sub-1': aspectRatio < 1, 'aspectRatio-1': aspectRatio == 1, 'aspectRatio-sub-2': aspectRatio > 1 && aspectRatio < 2, 'aspectRatio-2': aspectRatio == 2}" sizes="500px" class="img z-2" :src="img" @click.stop=""/>
        </q-card-section>
      </q-card>
    </q-dialog>
</template>

<style scoped lang="scss">
.img {
    position: absolute;
    object-fit: contain;
}

.aspectRatio-sub-1 {
    max-width: 500px;
    aspect-ratio: 2 / 3 ;
    object-fit: cover;
}

.aspectRatio-1 {
    max-width: 500px;
    aspect-ratio: 1 /1 ;
    object-fit: cover;
}

.aspectRatio-sub-2 {
    max-width: 700px;
    aspect-ratio: 3 / 2;
    object-fit: cover;
}

.aspectRatio-2 {
    max-width: 700px;
    aspect-ratio: 2 / 1;
    object-fit: cover;
}
</style>