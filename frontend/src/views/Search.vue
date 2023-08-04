<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers, type Ref, getCurrentInstance, type ComponentInternalInstance } from 'vue';
import type { User } from '@/assets/interfaces';
import { useStore } from '../store/store';
import { TouchSwipe } from 'quasar';
import Item from '../components/Item.vue';

import SearchBar from '@/components/SearchBar.vue';
export default defineComponent({
    props: {
        size: {
            type: Number,
            default: 1,
        },
        dense: {
            type: Boolean,
            default: false,
        },
        scrollPosition: {
            type: Number,
            default: 0,
        },
        height: {
            type: Number,
            default: 0,
        },
        query: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            results: new Array<User>(),
            users: new Array<User>(),
            input: ref(''),
            loading: false,
            noResults: false,
            q: this.$route.query.q as string,
            searchModal: false,
            alwaysTrue: this.$route.name == 'search',
            instance: null as ComponentInternalInstance | null,
            isDense: this.dense,
        };
    },
    name: 'search',
    setup() {
        const store = useStore()
    },
    created() {
        this.input = this.q;
        // this.search()
    },
    mounted() {
        this.instance = getCurrentInstance()
    },
    activated() {
        if(this.$q){
            this.input = this.q;
            this.search()
            this.instance = getCurrentInstance()
            this.alwaysTrue = true
        }
    },
    methods: {
      async search() {
        this.loading = true
        if(this.input === "") {
            this.results = new Array<User>()
            this.loading = false
            this.noResults = false
            return
        }
        http.get(`users/username/${this.input}`).then((res) => {
            if(res.data.success) {
                this.noResults = false
                this.results = res.data.users
            }
        }).catch((err) => {
            if(err.response.status === 404) {
                this.noResults = true
                this.results = new Array<User>()
            }
        })
        this.loading = false
      },
      resetInput() {
        this.input = ""
        this.results = new Array<User>()
        this.noResults = false
        const searchBar = this.$refs.bar as {
            resetInput: () => void
        }
        searchBar.resetInput()
      },
      submit() {
        this.$router.push({ name: 'search', query: { q: this.input } })
        this.resetInput()
      },
      searchFocus() {
        this.searchModal = true
      },
      closeSearch() {
        this.searchModal = false;
        this.resetInput()
      },
    },
    components: { Item, SearchBar },
    watch: {
        input(input) {
            if(input === "" || input == undefined) {
                this.results = new Array<User>()
                this.noResults = false
                return
            }
            this.search()
        },
    }
})
</script>


<template>
    <div v-if="instance?.parent?.type.name != 'KeepAlive'">
        <SearchBar search-page ref="bar" @update:focus="searchModal = $event" :dense="dense"/>
    </div>

    <div >
        <div class="results"  v-if="results.length > 0" v-for="u in results">
            <Item clickable :to="{ name: 'user-profile', params: { username: u.username } }" >
                <template #avatar>
                    <img v-if="u.avatar" :src="u.avatar" alt="profile pic" />
                    <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="profile pic plage holder" class="rounded-full" />
                </template>
                <template #title>
                    <span class="text-xl text-heading weight-900">
                        {{u.first_name + ' ' + u.last_name}}
                    </span>
                </template>
                <template #caption>@{{ u.username }}</template>
            </Item>
        </div>
    </div>
    <div>
        <q-dialog transition-show="false" transition-hide="false" v-if="$q.screen.lt.sm && searchModal && !($route.name == 'search')" class="w-full h-full modal" v-model="searchModal" :maximized="true">
            <div class="bg-theme w-full h-full">
                <div class="p-2">
                    <Item align-items="center" dense v-if="$store.state.authenticated" class="w-full overflow-visible bg-transparent">
                        <template #avatar>
                            <!-- <div :style="{width: '3rem', height: '3rem'}">
                            </div> -->
                            <q-btn v-if="$route.name != 'search'" size="20px" @click="closeSearch" flat dense round class="text-heading" icon="arrow_back" />
                            <q-btn v-else size="20px" @click="{resetInput(); $router.back()}" flat dense round class="text-heading" icon="arrow_back" />
                        </template>
                        <template #title>
                            <SearchBar ref="bar" autofocus @update:input="input = $event" search-page :dense="dense"/>
                        </template>
                        <template #icon>
                            <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
                        </template>
                    </Item>
                </div>

                <div>
                    <hr/>
                </div>

                <div >
                    <div class="results"  v-if="results.length > 0" v-for="u in results">
                        <Item clickable :to="{ name: 'user-profile', params: { username: u.username } }" >
                            <template #avatar>
                                <img v-if="u.avatar" :src="u.avatar" alt="profile pic" />
                                <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="profile pic plage holder" class="rounded-full" />
                            </template>
                            <template #title>
                                <span class="text-xl text-heading weight-900">
                                    {{u.first_name + ' ' + u.last_name}}
                                </span>
                            </template>
                            <template #caption>@{{ u.username }}</template>
                        </Item>
                    </div>
                </div>
            </div>
        </q-dialog>

        <q-dialog transition-show="false" transition-hide="false" v-if="$q.screen.lt.sm && $route.name == 'search'" class="w-full h-full modal" v-model="alwaysTrue" :maximized="true">
            <div class="bg-theme w-full h-full">
                <div class="p-2">
                    <Item align-items="center" dense v-if="$store.state.authenticated" class="w-full overflow-visible bg-transparent">
                        <template #avatar>
                            <!-- <div :style="{width: '3rem', height: '3rem'}">
                            </div> -->
                            <!-- <q-btn v-if="$route.name != 'search'" size="20px" @click="closeSearch" flat dense round class="text-heading" icon="arrow_back" /> -->
                            <q-btn size="20px" @click="{resetInput(); $router.back()}" flat dense round class="text-heading" icon="arrow_back" />
                        </template>
                        <template #title>
                            <SearchBar ref="bar" autofocus @update:input="input = $event" search-page :dense="true"/>
                        </template>
                        <template #icon>
                            <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
                        </template>
                    </Item>
                </div>

                <div>
                    <hr/>
                </div>

                <div >
                    <div class="results"  v-if="results.length > 0" v-for="u in results">
                        <Item clickable :to="{ name: 'user-profile', params: { username: u.username } }" >
                            <template #avatar>
                                <img v-if="u.avatar" :src="u.avatar" alt="profile pic" />
                                <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="profile pic plage holder" class="rounded-full" />
                            </template>
                            <template #title>
                                <span class="text-xl text-heading weight-900">
                                    {{u.first_name + ' ' + u.last_name}}
                                </span>
                            </template>
                            <template #caption>@{{ u.username }}</template>
                        </Item>
                    </div>
                </div>
            </div>
        </q-dialog>
    </div>
</template>

<style scoped lang="scss">

</style>