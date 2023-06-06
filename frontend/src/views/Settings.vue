<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Item from '../components/Item.vue'

// import imageCropper from '@/components/imageCropper.vue';

export default defineComponent({
    props: {
        
    },
    data() {
        return {
            imgURL: '',
            img: null
        }
    },
    setup() {
        const store = useStore()
        const {cookies} = useCookies();
        return {cookies};
    },
    methods: {
        async launchCropper(e: Event) {
            if(!e) return;
            var file = event?.target.files[0]
            this.img = await this.toBase64(file);
            console.log(this.$refs)
            this.$refs.cropperDialog.initCropper(file.type);
        },

        async toBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = (error) => reject(error);
            })
        },
    },
    created() {
    },
    components: { Item }
})
</script>

<template>
    <input ref="filePickerField" type="file" accept="image/*" @change="launchCropper" hidden/>

    <div>
        <q-avatar size="350px">
            <q-img :src="imgURL"></q-img>
        </q-avatar>
    </div>

    <q-btn @click="$refs.filePickerField.click()">
        upload
    </q-btn>

    <image-cropper ref="cropperDialog" :chosen-img="img" @onReset="$ref.filePickerField.value = null" @onCrop="(croppedImage) => {img = croppedImage}"/>
</template>

<style scoped>
</style>