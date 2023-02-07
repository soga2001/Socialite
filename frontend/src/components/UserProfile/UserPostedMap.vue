<script lang="ts">
import { defineComponent } from 'vue';
import type { Post } from '@/assets/interfaces';
import { http } from '@/assets/http';

export default defineComponent({
    props: {
        post: {type: Object as () => Post, required: true},
        // user_avatar: {type: String, required: true},
    },
    data() {
        return {
            id: this.post.id,
            username: this.post.username,
            user_id: this.post.user,
            img_url: this.post.img_url,
            caption: this.post.caption,
            date_posted: this.post.date_posted,
            date_updated: this.post.date_updated,
            avatar: this.user_avatar,
            dropdown: false,
            liked: false,
            comments: [],
            img_loading: true,
            avatar_loading: true
        }
    },
    methods: {
        report() {
            console.log('potato')
        },
        like() {
            console.log(this.liked)
            this.liked = !this.liked
        },
        onImgLoad() {
            this.img_loading = false
        },
        onAvatarLoaded() {
            this.avatar_loading = false
        },
    },
    created() {
    }
})
</script>

<template>
    <div>
        <!-- <img :src="img_url"/> -->
        <q-responsive :ratio="1" class="images">
            <img :src="img_url"/>
      </q-responsive>
    </div>
</template>


<style scoped>
img {
    object-fit: cover;
    border-radius: 10px;
}
</style>