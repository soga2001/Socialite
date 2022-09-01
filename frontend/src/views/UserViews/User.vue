<script lang="ts">
import { defineComponent } from 'vue';
import { http } from '@/assets/http';
import UserMap from './UserMap.vue';
import type { User } from '@/assets/interfaces';

export default defineComponent({
    data() {
        return {
            user_id: this.$route.query.id,
            user: new Array<User>(),
        };
    },
    methods: {
        userInfo() {
            http.get(`users/user/${(this.user_id)}/`).then((res) => {
                if (res.data.success) {
                    this.user = res.data.user;
                }
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    created() {
        this.userInfo();
    },
    components: { UserMap }
})
</script>

<template>
    <div v-for="u in user">
        <UserMap :user="u"/>
    </div>
</template>