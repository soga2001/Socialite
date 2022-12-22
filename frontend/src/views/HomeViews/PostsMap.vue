<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { Post } from '@/assets/interfaces';
import { http } from '@/assets/http';
import { Cookies, useQuasar } from 'quasar';


export default defineComponent({
    props: {
        post: {type: Object as () => Post, required: true}
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
            avatar: this.post.user_avatar,
            dropdown: false,
            liked: false,
            comments: [],
            img_loading: true,
            avatar_loading: true,
            delete: false,
            persistent: ref(false),
            report: ref(false),
            reason: ref('')
        }
    },
    methods: {
        reportPost() {
            console.log(this.reason)
        },
        like() {
            this.liked = !this.liked
            if(!this.$store.state.authenticated) return
        },
        setDelete() {
            this.delete = true
        },
        deletePost() {
            http.delete('posts/delete_post/', {
                data: {
                    id: this.id
                },
                headers: {
                'Authorization': `Bearer ${Cookies.get('access_token')}`
            }
            }).then((res) => {
                console.log(res)
            }).catch((err) => {
                console.log(err)
            })
        },
        onImgLoad() {
            this.img_loading = false
        },
        onAvatarLoaded() {
            this.avatar_loading = false
        },
    },
    created() {
        // http.get(`user_profile/get_profile/${this.user_id}/`).then((res) => {
        //     this.avatar = res.data.user_profile.avatar
        // }).catch((err) => {
        //     console.log(err)
        // })
    }
})
</script>

<template>
    <q-card class="post">
        <div class="post__main">
            <q-item class="post__info" :to="{path: 'profile/user', query: {id: user_id}}">
                <q-item-section avatar>
                <q-avatar size="50px">
                    <img v-if="avatar" :src="avatar"/>
                    <q-icon v-else size="50px" name="face" />
                </q-avatar>
                </q-item-section>

                <q-item-section>
                <q-item-label class="username">@{{username}}</q-item-label>
                <q-item-label caption class="date__posted">
                    <timeago :datetime="date_posted"  auto-update :converter-options="{ includeSeconds: true, addSuffix: true, useStrict: false,}"/>
                </q-item-label>
                </q-item-section>
            </q-item>

        <div class="dropdown__div">
                <q-btn size="16px" class="more__vert" flat dense round icon="more_vert" />
                <q-menu class="dropdown" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                    <q-list class="more__option">
                        <q-item clickable v-close-popup @click="report = true" v-if="username !== $store.state.user.username">
                            <q-item-section avatar>
                                <q-icon class="danger__icon" name="flag"/>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>Report Post</q-item-label>
                            </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="username === $store.state.user.username">
                            <q-item-section avatar>
                                <q-icon class="danger__icon" name="delete_forever"/>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>Delete</q-item-label>
                            </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup v-if="username === $store.state.user.username">
                            <q-item-section avatar>
                                <q-icon class="" name="edit_note"/>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>Edit</q-item-label>
                            </q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
                <!-- Confirm Delete Model -->
                <q-dialog v-model="persistent" persistent transition-show="scale" transition-hide="scale">
                    <q-card class="card">
                        <q-card-section class="row">
                            <q-item>
                                <q-item-section class="title">Are you sure you want to delete this post?</q-item-section>
                            </q-item>
                        </q-card-section>
                        <q-card-section>
                            <q-item>
                                <q-item-section avatar>
                                <q-avatar class="red" icon="warning"/>
                                </q-item-section>
                                <q-item-section class="red alert">This action is permanent and irreversible.</q-item-section>
                            </q-item>
                        </q-card-section>

                        <q-card-actions align="right" class="buttons">
                            <q-btn flat label="Cancel"  v-close-popup />
                            <q-btn flat label="Confirm" @click="deletePost" v-close-popup />
                        </q-card-actions>
                    </q-card>
                </q-dialog>
                <!-- Report model -->
                <q-dialog v-model="report" persistent>
                    <q-card class="card">
                        <q-card-section>
                            <!-- <h6 class="title">Report</h6> -->
                            <q-item>
                                <q-item-section class="title">Report</q-item-section>
                                <q-item-section avatar>
                                <q-avatar class="red" icon="flag"/>
                                </q-item-section>
                            </q-item>
                        </q-card-section>
                        <q-card-section class="q-pt-none">
                            <!-- <q-input :dark="$store.state.dark" class="report__reason" placeholder="Reason" dense v-model="reason" /> -->
                            <q-input
                                v-model="reason"
                                filled
                                clearable
                                type="textarea"
                                label="Reason"
                                :dark="$store.state.dark"                                
                            />
                        </q-card-section>

                        <q-card-actions align="right" class="buttons">
                            <q-btn flat label="Cancel" v-close-popup />
                            <q-btn flat label="Report" v-close-popup @click="reportPost" />
                        </q-card-actions>
                    </q-card>
                </q-dialog>
            </div>
        </div>  
        <!-- <div class="caption" v-if="caption">
            <span class="post__caption">{{ caption }}</span>
        </div> -->
        <q-img :src="img_url" />
        <q-item-section v-if="caption" class="caption">
            <q-item-label><span class="caption__username">{{ username }}</span></q-item-label>
            <q-item-label caption class="post__caption">{{caption}}</q-item-label>
        </q-item-section>
            
        <q-card-actions>
            <!-- <q-btn flat round color="red" :icon="liked ? 'favorite' : 'favorite_border'" /> -->
            <q-btn round flat class="like__btn" :icon="liked ? 'favorite' : 'favorite_border'" :disable="!$store.state.authenticated" v-on:click="like">
                <q-tooltip :offset="[0,0]">
                    Like
                </q-tooltip>
            </q-btn>
            <q-btn icon="chat" round flat>
                <q-tooltip :offset="[0,0]">
                    Comment
                </q-tooltip>
            </q-btn>
            <q-btn icon="share" round flat>
                <q-tooltip :offset="[0,0]">
                    Copy Link
                </q-tooltip>
            </q-btn> 
        </q-card-actions>
        <q-separator :dark="$store.state.dark"/>
        <div class="comments">
            <p>Comments</p>
            <q-item v-if="caption">
                <q-item-section avatar>
                <q-avatar>
                    <img :src="avatar">
                </q-avatar>
                </q-item-section>

                <q-item-section>
                <q-item-label><span class="caption__username">{{ username }}</span> <span><timeago :datetime="date_posted"  auto-update :converter-options="{ includeSeconds: true, addSuffix: true, useStrict: false,}"/></span></q-item-label>
                <!-- <q-item-label caption class="post__caption">{{caption}}</q-item-label> -->
                <q-item-label caption class="post__caption">Some comment</q-item-label>

                </q-item-section>
            </q-item>
        </div>
        <!-- <div>
            <q-item v-if="caption">
                <q-item-section avatar>
                <q-avatar>
                    <img :src="avatar">
                </q-avatar>
                </q-item-section>

                <q-item-section>
                <q-item-label><span class="caption__username">{{ username }}</span> <span><timeago :datetime="date_posted"  auto-update :converter-options="{ includeSeconds: true, addSuffix: true, useStrict: false,}"/></span></q-item-label>
                <q-item-label caption class="post__caption">{{caption}}</q-item-label>
                </q-item-section>
            </q-item>
        </div> -->
    </q-card>
</template>

<style scoped>
.post {
    margin: 30px auto;
    display: grid;
    background-color: var(--color-background-soft);
    position: relative;
    min-width: 500px;
    max-width: 600px;
    box-shadow:0 4px 20px 0 var(--color-text);
    height: 100%;
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
    font-weight: bold;
}

.date__posted {
    font-size: 12px;
    color: var(--color-text);
}


.dropdown__div {
    display: flex;
    justify-content: center;
    justify-items: center;
    align-items: center;
    align-content: center;
}

/* .dropdown {
    box-shadow: 0 4px 8px 0 var(--color-heading), 0 6px 20px 0 var(--color-heading);
} */

.more__vert {
    color: var(--color-heading);
    background-color: transparent;
    box-shadow: none !important;
    display: flex;
    float: right;
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

.post__img {
    width: 100%;
}


.footer {
    padding: 15px 20px;
}
.post__interact {
    display: flex;
}

.like__btn {
    color: red;
}

.skeleton {
    color: var(--color-text);
}


.post__interact h3 {
    padding: 10px;
}

.card {
    background-color: var(--color-background);
    box-shadow:0 4px 20px 0 var(--color-border);
    width: 100%;
    max-width: 500px;
}

.title {
    color: var(--color-heading) !important;
    font-weight: 900;
    font-size: 20px;
}

.confirm__divider {
    background-color: var(--color-border);
}

.confirm__text {
    color: var(--color-heading);
}

.buttons {
    color: var(--color-heading);
}

.red {
    color: red;
}

.alert {
    font-size: 15px;
}

.report__reason {
    background-color: var(--color-background);
    color: var(--color-heading) !important;
}

::placeholder {
    /* color: var(--color-heading) !important; */
    color: red !important;
}


.caption {
    padding: 15px 15px !important;
}

.caption__username {
    font-weight: bolder;
    color: var(--color-heading);
}

.post__caption {
    font-weight: 500;
    color: var(--color-text);
}
.comments {
    padding: 5px 15px;
    color: var(--color-heading);
}
</style>