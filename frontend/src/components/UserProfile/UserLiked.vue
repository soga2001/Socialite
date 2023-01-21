<script lang="ts">
import type { Post } from '@/assets/interfaces';
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'User_Liked',
    props: {
        user_avatar: {type: String, required: true}
    },
    data() {
        return {
            user_id: this.$route.query.id,
            user_timestap: new Date().toISOString(),
            user_posted: new Array<Post>(),
            avatar: this.user_avatar
        };
    },
})
</script>

<template>
    <div class="user__liked__main">
        <div class="user__liked">
            <!-- <div class="grid" v-if="user_posted.length > 0" v-for="post in user_posted" :key="post.id">
                <UserPostedMap class="post" :post="post" :user_avatar="avatar"/>
            </div> -->
            <q-icon size="100px" name="las la-folder-open" />
            <h4>User has liked no Posts</h4>
        </div>
    </div>
</template>

<style scoped>
.user__liked__main {
    text-align: center;
    display: flex;
    justify-content: center;
    justify-self: center;
    align-items: center;
    align-self: center;
    height: 100%;
}
</style>