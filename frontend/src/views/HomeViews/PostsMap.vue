<script lang="ts">
import { defineComponent } from 'vue';
import type { Post } from '@/assets/interfaces';
import { http } from '@/assets/http';
import type { date } from 'quasar';

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
            dropdown: false
        }
    },
    methods: {
        report() {
            console.log('potato')
        }
    },
    created() {
        // not sure if this works
        http.get(`user_profile/get_profile/${this.user_id}/`).then((res) => {
            this.avatar = res.data.user_profile.avatar
        }).catch((err) => {
            console.log(err)
        })
        console.log(this.$store.state.user)
    }
})
</script>

<template>
    <div class="post">
        <div class="post__head__div">
            <!-- <RouterLink :to="'profile/user?id='+ user_id" class="post__header">
                @{{username}}
            </RouterLink> -->
            <div class="post__main">
                <q-item clickable class="post__info" v-on:click="$router.push(`profile/user?id=${user_id}`)">
                    <q-item-section avatar>
                        <q-avatar color="secondary" text-color="white">
                            <img :src="avatar" />
                        </q-avatar>
                    </q-item-section>
                    <q-item-section>
                        <q-item-label class="username">@{{username}}</q-item-label>
                        <q-item-label caption class="date__posted"><timeago :datetime="date_posted"/></q-item-label>
                    </q-item-section>
                </q-item>
                <div class="dropdown__div">
                    <q-icon class="more__vert" name="more_vert"/>
                    <q-menu v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                        <q-list class="more__option">
                            <q-item clickable v-close-popup v-if="!$store.state.authenticated && username !== $store.state.user.username">
                                <q-item-section avatar>
                                    <q-icon class="danger__icon" name="report_problem"/>
                                </q-item-section>
                                <q-item-section>
                                    <q-item-label>Report Post</q-item-label>
                                </q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup v-if="username === $store.state.user.username">
                                <q-item-section avatar>
                                    <q-icon class="danger__icon" name="delete"/>
                                </q-item-section>
                                <q-item-section>
                                    <q-item-label>Delete</q-item-label>
                                </q-item-section>
                            </q-item>

                            <q-item clickable v-close-popup v-if="username === $store.state.user.username">
                                <q-item-section avatar>
                                    <q-icon class="" name="edit"/>
                                </q-item-section>
                                <q-item-section>
                                    <q-item-label>Edit</q-item-label>
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                </div>
            </div>
        </div>
        <img :src="img_url" />
        <div class="footer">
            <div class="post__interact">
                <button disabled>Like</button>
                <button disabled>Comment</button>
                <button disabled>Share</button>
            </div>
            <hr/>
            <span><RouterLink :to="'profile/user?id='+ user_id" class="post__caption">{{username}}</RouterLink>: {{caption}}</span>
        </div>
    </div>
</template>

<style scoped>
.post {
    margin: 60px auto;
    display: grid;
    background-color: var(--color-background-soft);
    position: relative;
    min-width: 500px;
    max-width: 600px;
}

.post__head__div {
    display: flex, table-cell;
    position: relative;
}

.post__main {
    display: grid;
    grid-template-columns: 1fr auto;

}
.post__info {
    padding: 5px 10px;
    background-color: transparent;
}

.username {
    font-size: 20px;
    color: var(--color-heading);
}

.date__posted {
    font-size: 12px;
    color: var(--color-text);
}

.more__vert {
    color: var(--color-heading);
    width: fit-content;
    font-size: 20px;
    height: 100%;
    background-color: transparent;
    box-shadow: none !important;
    border-radius: 0;
    display: flex;
    align-items: center;
    align-items: center;
    cursor: pointer;
}

.more__option {
    background-color: var(--color-background-mute);
    color: var(--color-heading);
}

.danger__icon {
    color: rgb(244, 106, 106);
}

img {
    width: 100%;
}


.footer {
    padding: 15px 20px;
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