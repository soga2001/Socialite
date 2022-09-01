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
        <div class="mapping__head__div">
            <RouterLink :to="'user?id='+ user_id" class="mapping__header">@{{username}}</RouterLink>
            <select class="mapping__dropdown">
                <option>Options Here</option>
            </select>
        </div>
        <img :src="img_url" />
        <div class="mapping__interact">
            <h3>Like</h3>
            <h3>Comment</h3>
            <h3>Share</h3>
        </div>
        <hr/>
        <span><RouterLink :to="'user?id='+ user_id" class="mapping__caption">{{username}}</RouterLink>: {{caption}}</span>
    </div>
</template>

<style scoped>
.mapping {
    /* text-align: center; */
    border: 2px solid var(--color-border);
    margin: 10px auto;
    width: fit-content;
    padding: 20px;
    display: grid;
    background-color: var(--color-background-soft);
}

.mapping__head__div {
    display: flex;
    position: relative;
}
.mapping__header {
    text-align:left;
    color: var(--color-text);
    font-size: 30px;
    border: 0;
    border-width: 0px;
}

.mapping__dropdown {
    position: absolute;
    right: 0;
    /* padding: 20px; */
    bottom: 0;
    top: 0;
    border: 0;
    border-width: 0px;
    background-color: var(--color-background-soft);
    color: var(--color-text)
}

select:focus {
    border: 0;
    border-width: 0px;
}

select option:checked {
    border: 0;
    border-width: 0px;
}

select:active {
    border: 0;
    border-width: 0px;
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