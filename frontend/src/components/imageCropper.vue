<script lang="ts">
  import { defineComponent, ref, reactive, onUnmounted } from "vue";
  import { Cropper, RectangleStencil, CircleStencil } from "vue-advanced-cropper";
  import "vue-advanced-cropper/dist/style.css";
  import 'vue-advanced-cropper/dist/theme.compact.css';
  
  export default defineComponent({
    components: {
        Cropper,
        RectangleStencil,
        CircleStencil,
    },
    props: {
        circle: {
            type: Boolean,
            default: false,
        },
        aspectRatio: {
            type: Number,
            default: 3/1,
        },
        chosenImg: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            showCropper: false,
            imgFileType: '',
            fileName: '',
        }
    },
    computed: {
        stencilClass() {
            return this.circle ? 'circle' : 'normal';
        },
        stencilComponent() {
            return this.circle ? CircleStencil : RectangleStencil;
        },
        theme() {
            return this.$store.state.dark;
        },
    },
    methods: {
        async initCropper(imageFileType: any, filename: string) {
            this.showCropper = true;
            this.imgFileType = imageFileType
            this.fileName = filename
            await new Promise(resolve => setTimeout(resolve, 50));
            // // this.$refs.cropper.replace(this.chosenImg)
        },
        cropImage() {
            const { canvas } = (this.$refs.cropper as any).getResult();
			canvas.toBlob((blob: Blob) => {
				// Do something with blob: upload to a server, download and etc.
                const file = new File([blob], this.fileName, { type: this.imgFileType });
                const croppedImg = canvas.toDataURL(this.imgFileType)

                this.$emit("file", file)
                this.$emit("onCrop", croppedImg);
                this.resetCropper();
			}, this.imgFileType);
        },
        async resetCropper() {
            this.showCropper = false;
            this.imgFileType = '';
            
            await new Promise(resolve => setTimeout(resolve, 50));
            if(this.$refs.cropper) {
                (this.$refs.cropper as any).replace(null)
            }
            this.$emit('onReset')
        },
    },
  });
  </script>

<template>
    <!-- <div id="app">
        <cropper
			ref="cropper"
			class="coodinates-cropper"
			:src="img.src"
            default-boundaries="fill"
            check-orientation
			:stencil-props="{
                aspectRatio: aspectRatio,
                previewClass: stencilClass
			}"
            :stencil-component="stencilComponent"
		/>
        <div class="button-wrapper">
            <button class="button" @click="cropImage()">Crop image</button>
        </div>
    </div> -->
    <div class="crop-image-dialog relative w-full h-full">
        <q-dialog :dark="theme" v-model="showCropper" class="w-full h-full" persistent>
            <q-card :dark="theme" class="w-full">
                <q-card-section>
                    <Item dense :vert-icon-center="true">
                        <template #title>
                            <div class="text-lg">Edit Window</div>
                        </template>
                        <template #icon>
                            <i-close class="btn" :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem" @click="resetCropper"/>
                        </template>
                    </Item>
                    
                </q-card-section>
                <q-card-section>
                    <!-- <cropper ref="cropper" class="w-full" :aspect-ratio="aspectRatio" :guides="true" :background="false" :view-mode="3" drag-mode="move" @ready="" :src="chosenImg" alt="Image not available"/> -->
                    <cropper
                        ref="cropper"
                        class="coodinates-cropper"
                        :src="chosenImg"
                        default-boundaries="fill"
                        check-orientation
                        :stencil-props="{
                            aspectRatio: aspectRatio,
                            previewClass: stencilClass
                        }"
                        :stencil-component="stencilComponent"
                    />
                </q-card-section>
                <q-card-actions class="justify-center">
                    <q-btn class="btn-themed" @click="cropImage" >Crop</q-btn>
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
  </template>
  
  
  
  <style>
  #app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  
  .coodinates-cropper {
    width: 100%;
    height: fit-content;
  }

  .normal {
    width: 100%;
    height: 100%;
  }

  .circle {
    border-radius: 50%;
    overflow: hidden;

  }
  
  .button-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 17px;
  }
  
  .button {
    color: white;
    font-size: 16px;
    padding: 10px 20px;
    width: 100%;
    background: #151515;
    cursor: pointer;
    transition: background 0.5s;
    border: none;
  }
.button:not(:last-of-type) {
      margin-right: 10px;
    }
    .button:hover {
      background: #2F2F2F;
    }
    .button input {
      display: none;
    }
</style>
