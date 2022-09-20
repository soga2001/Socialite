<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
export default defineComponent({
    data() {
        return {
            users: new Array<User>(),
            input: ref('')
        };
    },
    created() {

    },
    methods: {
      async search() {
        const temp = this.input
        this.input = ""
        http.get(`users/username/${(temp)}`).then((res) => {
            if(res.data.success) {
                this.users = res.data.users
                console.log(this.users)
            }
            else {
                this.input = temp
            }
        })
        // this.users = users.data.users
      }
    }
})
</script>


<template>
    <div class="home__sides__main">
        <h1>Stuff</h1>
        <form v-on:submit.prevent="search">
            <input type="search" placeholder="search" v-debounce:1s.cancelonempty="search" v-model='input' required/>
        </form>
    </div>
</template>

<style scoped>
    
</style>