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
            edit: false,
        }
    },
    methods: {

    },
})
</script>

<template>
    <div>
        <Item class="bg-theme h-full w-full" alignItems="start" :captionLineClamp="4">
            <template #avatar>
                <img class="pointer hover-darker" @click="$router.push({name: 'user-profile', params: {username: comment.username}})"  v-if="comment.user_avatar" :src="comment.user_avatar"/>
                <!-- <ProfileIcon v-else/> -->
            </template>
            <template #title>
                <div class="w-full flex flex-cols gap-1 items-center">
                    <div>
                        <span class="text-xl pointer hover-underline text-heading weight-900"  @click="$router.push({name: 'user-profile', params: {username: comment.username}})">@{{ comment.username }}</span>
                    </div>
                    <span>&#183;</span>
                    <div>
                        <Timeago class="text-xs text-ligher weight-ligher" :date="comment.date_posted"/>
                    </div>
                    <div v-if="comment.date_updated" class="text-xs text-ligher weight-ligher">
                        (edited)
                    </div>
                </div>
            </template>
            <template #caption>
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