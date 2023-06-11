<script lang="ts">
import { defineComponent} from "vue";

export default defineComponent({
    name: 'unauthenticated',
    data() {
        return {

        }
    },
    methods: {

    },
})

</script>

<template>
    <div class="grid w-full h-full px-2 pt-2 pb-4 gap-2">
        <div class="text-xl text-heading">New to Socialite?</div>
        <div class="flex flex-col gap-3">
            <div class="text-sm text-body">Sign up now to listen to tea spilled by your friends.</div>
            <div class="w-full flex gap-2 bg-themed text-center">
                <RouterLink to="/login" class="w-full py-2 px-10 text-xl btn-themed rounded-lg no-decor">
                    Log in
                </RouterLink>
                <RouterLink to="/register" class="w-full py-2 px-10 text-xl border rounded-lg no-decor">
                    Sign up
                </RouterLink>
            </div>
        </div>
        

    </div>
</template>

<style scoped>

</style>