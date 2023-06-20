<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { Comment } from '@/assets/interfaces'
import { http } from '@/assets/http';


export default defineComponent({
    name: 'comment-map',
    props: {
        comment: {
            type: Object as () => Comment,
            required: true
        }
    },
    data() {
        return {
            edit: false,
            websocket: new WebSocket(`wss://localhost:8000/ws/comment/${this.comment.id}/`),
            dropdown: false,
            report: ref(false),
            reason: ref(""),
            deleteModal: false,
            deleted: false,
            deletedMsg: '',
            commentData: this.comment
        }
    },
    methods: {
        deleteComment() {
            http.delete(`comments/comment/${this.commentData.id}/`).then((res) => {
                console.log(res.data)
            }).catch((err) => {
                console.log(err);
            });
        },
        reportPost() {
            console.log(this.reason);
        },
        async websocketOpen() {
            this.websocket = new WebSocket(`wss://localhost:8000/ws/comment/${this.comment.id}/`)
            this.websocket.onopen = (e) => {
                console.log('Websocket opened')
            }
        },
        async websocketMessage() {
            this.websocket.onmessage = (e) => {
                console.log(e.data)
                const data = JSON.parse(e.data)
                if(data.type == "delete") {
                    this.deleted = true
                    this.deletedMsg = data.message
                }
            }
        },
        async websocketClose() {
            this.websocket.close()

            this.websocket.onclose = (e) => {
                console.log('Websocket closed')
            }
        },
    },
    mounted() {
        this.websocketOpen()
        this.websocketMessage()
    },
    unmounted() {
        this.websocketClose()
    },
    watch: {
        commentData: {
            handler: function(val, oldVal) {
                this.websocketMessage()
            },
            deep: true
        },
        deleted(deleted) {
            if(deleted) {
                this.websocket.close()
            }
        }
    }
})
</script>

<template>
    <div v-if="!deleted">
        <Item class="bg-theme h-full w-full" alignItems="start" :captionLineClamp="4">
            <template #avatar>
                <img class="pointer hover-darker" @click="$router.push({name: 'user-profile', params: {username: commentData.username}})"  v-if="commentData.user_avatar" :src="commentData.user_avatar"/>
                <!-- <ProfileIcon v-else/> -->
            </template>
            <template #title>
                <div class="w-full flex flex-cols gap-1 items-center">
                    <div>
                        <span class="text-xl pointer hover-underline text-heading weight-900"  @click="$router.push({name: 'user-profile', params: {username: commentData.username}})">@{{ commentData.username }}</span>
                    </div>
                    <span>&#183;</span>
                    <div>
                        <Timeago class="text-xs text-ligher weight-ligher" :date="commentData.date_posted"/>
                    </div>
                    <div v-if="commentData.date_updated" class="text-xs text-ligher weight-ligher">
                        (edited)
                    </div>
                </div>
            </template>
            <template #caption>
                <div class="text-base w-fit" @click.stop="" >
                    <MentionLink :mention="commentData.comment"/>
                </div>
            </template>
            <template #icon>
                <div>
                        <q-btn @click.stop="dropdown = !dropdown" size="13px" class="more__vert" flat round>
                            <q-icon name="more_horiz" class="btn-hover-theme" />
                        </q-btn>
                        <q-menu class="dropdown" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                            <q-list class="more__option">
                                <q-item clickable v-close-popup @click="report = true" v-if="commentData.username !== $store.state.user.username">
                                    <q-item-section avatar>
                                        <q-icon class="danger__icon" name="flag"/>
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>Report Post</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item clickable v-close-popup @click="deleteModal = true" tabindex="0" v-if="commentData.username === $store.state.user.username">
                                    <q-item-section avatar>
                                        <q-icon class="danger__icon" name="delete_forever"/>
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>Delete</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item clickable v-close-popup v-if="commentData.username === $store.state.user.username">
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
                        <q-dialog v-model="deleteModal" persistent transition-show="scale" transition-hide="scale">
                            <q-card class="card">
                                <q-card-section class="row">
                                    <q-item>
                                        <q-item-section class="title">Are you sure you want to delete this comment?</q-item-section>
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
                                    <q-btn flat label="Confirm" @click="deleteComment" v-close-popup />
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
            </template>
        </Item>
    </div>
    <div v-if="deleted" class=" flex justify-center items-center h-full w-full">
        <Item>
            <template #title>
                <div class="">
                    <span class="text-xl">{{ deletedMsg }}</span>
                </div>
            </template>
        </Item>
    </div>
</template>

<style scoped>
</style>