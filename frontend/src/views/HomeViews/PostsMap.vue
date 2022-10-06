<script lang="ts">
import { defineComponent } from 'vue';
import type { Post } from '@/assets/interfaces';
import { http } from '@/assets/http';

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
            date_updated: this.post.date_updated,
            avatar: '',
        }
    },
    // methods: {

    // }
    created() {
        // not sure if this works
        http.get(`user_profile/get_profile/${this.id}/`).then((res) => {
            this.avatar = res.data.user_profile.avatar
        }).catch((err) => {
            console.log(err)
        })
    }
})
</script>

<template>
    <div class="post">
        <div class="post__head__div">
            <RouterLink :to="'user?id='+ user_id" class="post__header">
                @{{username}}
            </RouterLink>
            <span class="posted__date">&#x2022
                <timeago :datetime="date_posted"/>
                {{date_updated ? "&#x2022 (edited)" : ""}}
            </span>
            <select class="post__dropdown">
                <option>Options Here</option>
            </select>
        </div>
        <img :src="img_url" />
        <div class="post__interact">
            <h3>Like</h3>
            <h3>Comment</h3>
            <h3>Share</h3>
        </div>
        <hr/>
        <span><RouterLink :to="'user?id='+ user_id" class="post__caption">{{username}}</RouterLink>: {{caption}}</span>
    </div>
</template>

<style scoped>
.post {
    /* text-align: center; */
    border-top: 2px solid var(--color-border);
    border-bottom: 2px solid var(--color-border);
    margin: 10px auto;
    /* width: fit-content; */
    padding: 20px;
    display: grid;
    background-color: var(--color-background-soft);
    position: relative;
}

.post__head__div {
    display: flex, table-cell;
    position: relative;
}
.post__header {
    text-align:left;
    color: var(--color-heading);
    font-size: 20px;
    border: 0;
    border-width: 0px;
}

.posted__date {
    font-size: 20px;
    color: var(--color- );
    margin-left: 5px;
}

.post__dropdown {
    position: absolute;
    right: 0;
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
    max-width: 100%;
}

.post__interact {
    display: flex;
}

.post__interact h3 {
    padding: 10px;
}

.post__caption {
    text-align: left;
}
</style>