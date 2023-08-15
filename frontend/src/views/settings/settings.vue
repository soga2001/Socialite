<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'settings',
    props:{
        scrollPosition: {
            type: Number,
            default: 0,
        },
        height: {
            type: Number,
            default: 0,
        }
    },
    data() {
        return {
            hide: false,
        }
    },
    methods: {

    },
    mounted() {

    },
    watch: {
        '$route': function() {
            // const route =  this.$route.name ?? ''
            // console.log(this.$q.screen.lt.sm)
            // if (this.$route.matched[1].name && this.$q.screen.lt.sm) {
            //     this.hide = true
            // }
            // else if(this.$route.matched[1] == undefined) {
            //     this.hide = false
            // }
        },
    },
})
</script>

<template>
    <div :class="{'cols-2': !hide}" class="grid w-full min-h-viewport">
        <header class="border-r h-full w-full" v-if="!hide">
            <div>
                <Item>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading px-2 py-2">
                            Settings
                        </span>
                    </template>
                </Item>
            </div>
            
            <nav class="w-full">
                <RouterLink :to="{name: 'account'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Account
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Change your password, email, username, or deactive account
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink :to="{name: 'notifications'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Notifications
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Turn off notifications from users you follow
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
            </nav>
        </header>
        <div class="w-full">
            <RouterView class="w-full" />
        </div>
    </div>
</template>


<style scoped lang="scss">
* {
    text-decoration: none;
}

.active {
    
    .child {
        background-color: #f5f5f5;
    }
}
</style>