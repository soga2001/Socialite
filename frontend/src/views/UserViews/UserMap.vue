<script lang="ts">
import { defineComponent, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';

export default defineComponent({
    props: {
        user: {type: Object as () => User, required: true}
    },
    data() {
        return {
            id: this.user.id,
            username: this.user.username,
            email: this.user.email,
            first_name: this.user.first_name,
            last_name: this.user.last_name,
            is_active: this.user.is_active,
            is_staff: this.user.is_staff,
            is_superuser: this.user.is_superuser,
            last_login: this.user.last_login
        }
    },
    methods: {
        maskEmail() {

        }
    }
})
</script>

<template>
    <div>
        <h1>User: {{username}}</h1>
        <h3>{{first_name}} {{last_name}}</h3>
        <h4>Is Active: {{is_active}}</h4>
        <h5>Last logged in: {{last_login}}</h5>
    </div>
</template>

<style scoped>

div {
    display: grid;
}
    
</style>