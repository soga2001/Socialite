<script lang="ts">
import { defineComponent } from 'vue';
import type { Comment } from '@/assets/interfaces'


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

        }
    },
    methods: {

    },
})
</script>

<template>
    <div>
        <Item class="bg-theme" alignItems="start" :captionLineClamp="4">
            <template #avatar>
                <img class="pointer hover-darker" @click="$router.push({name: 'user-profile', params: {username: comment.username}})"  v-if="comment.user_avatar" :src="comment.user_avatar"/>
                <!-- <ProfileIcon v-else/> -->
            </template>
            <template #title>
                <div class="w-full">
                    <span class="text-xl pointer hover-underline"  @click="$router.push({name: 'user-profile', params: {username: comment.username}})">@{{ comment.username }}</span>
                </div>
            </template>
            <template #caption>
                <div class="flex">
                    <span class="text-xs"><Timeago size="12px" :date="comment.date_posted"/> </span>
                </div>
                <div class="text-base w-fit" @click.stop="" >
                    <MentionLink :mention="comment.comment"/>
                </div>
            </template>
            <template #icon>
                <div>
                    <q-btn flat dense round>
                        <q-icon class="btn-hover-theme" name="more_horiz" />
                    </q-btn>
                </div>
            </template>
        </Item>
    </div>
</template>

<style scoped>
</style>