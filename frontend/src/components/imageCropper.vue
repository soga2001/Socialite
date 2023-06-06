<script lang="ts">
import { constants } from 'buffer';
import { defineComponent, type CSSProperties, ref } from 'vue';

export default defineComponent({
    props: {
        aspectRatio: {
            default: 1/1
        },
        chosenImg: {
            default: null,
        },
    },
    data() {
        return {
            showCropper: false,
            imgFileType: null,
            fileName: null,
            // imgFile: null,
            // cropper: ref<any>(),
        }
    },
    methods: {
        async initCropper(imageFileType: any, filename: string) {
            console.log(filename)
            this.showCropper = true;
            this.imgFileType = imageFileType
            this.fileName = filename
            await new Promise(resolve => setTimeout(resolve, 50));
            this.$refs.cropper.replace(this.chosenImg)
        },

        async resetCropper() {
            this.showCropper = false;
            this.imgFileType = null;
            await new Promise(resolve => setTimeout(resolve, 50));
            if(this.$refs.cropper) {
                this.$refs.cropper.replace(null)
            }
            this.$emit('onReset')
        },
        onClose() {
            this.$emit('close');
            this.resetCropper();
        },
        async cropChosenImage() {
            const croppedImg = this.$refs.cropper.getCroppedCanvas().toDataURL(this.imgFileType)
            const file = await this.toFile(croppedImg)
            this.$emit("file", file)
            this.$emit("onCrop", croppedImg);
            this.resetCropper();
        },
        async toFile(uri: string) {
            var parts = uri.split(',');

            // Extract the mime type.
            var mimeType = parts[0].split(':')[1];
            console.log(mimeType)

            // Extract the base64 encoded data.
            var base64Data = parts[1];

            // Convert the base64 encoded data to a binary string.
            var binaryData = atob(base64Data);
            // Create a Blob object from the binary data
            const blob = await new Blob([binaryData], { type: mimeType });

            // Create a File object from the Blob object
            const file = await new File([blob], this.fileName, { type: this.imgFileType });

            return file;
        }

    },
})
</script>

<template>
    <div class="crop-image-dialog relative w-full h-full">
        <q-dialog dark v-model="showCropper" class="w-full h-full" persistent>
            <q-card dark class="w-full">
                <q-card-section>
                    <Item dense :vert-icon-center="true">
                        <template #title>
                            <div class="text-lg">Edit Window</div>
                        </template>
                        <template #icon>
                            <i-close size="2rem" class="btn" @click="onClose"/>
                        </template>
                    </Item>
                    
                </q-card-section>
                <q-card-section class="h-fit">
                    <cropper ref="cropper" :aspect-ratio="aspectRatio" :guides="true" :background="false" :view-mode="3" drag-mode="move" :src="chosenImg" alt="Image not available"/>
                </q-card-section>
                <q-card-actions class="justify-center">
                    <q-btn class="btn-themed" @click="cropChosenImage" >Crop</q-btn>
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>


<style scoped>

</style>