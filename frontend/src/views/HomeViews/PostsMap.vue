<script lang="ts">
import { defineComponent } from 'vue';
import type { Post } from '@/assets/interfaces';


export default defineComponent({
    props: {
        post: {type: Object as () => Post, required: true}
    },
    data() {
        return {
            id: this.post.id,
            username: this.post.username,
            user_id: this.post.user_id,
            img_url: this.post.img_url,
            caption: this.post.caption,
            date_posted: this.post.date_posted,
            date_updated: this.post.date_updated
        }
    }
})
</script>

<template>
    <div class="mapping">
        <RouterLink :to="'user?id='+ user_id" class="mapping__header">@{{username}}</RouterLink>
        <img :src="img_url" />
        <div class="mapping__interact">
            <h3>Like</h3>
            <h3>Comment</h3>
            <h3>Share</h3>
        </div>
        <hr/>
        <p class="mapping__caption">{{username}}: {{caption}}</p>
    </div>
</template>

<style scoped>
.mapping {
    text-align: center;
    border: 2px solid var(--color-border);
    margin: 10px auto;
    width: fit-content;
    padding: 20px;
    display: grid;
    background-color: var(--color-background-soft);
}

.mapping__header {
    text-align:left;
    color: var(--color-text);
    font-size: 30px;
}

img {
    width: 500px;
    max-height: 500px;
}

.mapping__interact {
    display: flex;
}

.mapping__interact h3 {
    padding: 10px;
}

.mapping__caption {
    text-align: left;;
}
</style>