<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { useStore } from '../store/store';
import { TouchSwipe } from 'quasar';
import Item from '../components/Item.vue';

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
        searchPage: {
            type: Boolean,
            default: false,
        },
        autofocus: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {
            results: new Array<User>(),
            users: new Array<User>(),
            input: '',
            loading: false,
            noResults: false,
            hasResults: false,

        };
    },
    name: 'search-bar',
    created() {
        if(this.$route.name == 'search') {
            this.input = this.$route.query.q as string;
        }
    },
    mounted() {
    },
    methods: {
      async search() {
        if(this.searchPage) {
            return
        }
        this.loading = true
        if(this.input === "") {
            this.results = new Array<User>()
            this.loading = false
            this.noResults = false
            return
        }
        http.get(`users/username/${this.input}`).then((res) => {
            console.log(res)
            if(res.data.success) {
                this.noResults = false
                this.results = res.data.users
                this.hasResults = true;
            }
            console.log('here')
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
        this.hasResults = false
      },
      submit() {
        this.$router.push({ name: 'search', query: { q: this.input } })
        this.resetInput()
      },
      blur() {
        this.resetInput();
        this.$emit('update:focus', false);
        (this.$refs.input as HTMLInputElement).blur();
      },
      onFocus() {
        this.$emit('update:focus', true);
        // (this.$refs.input as HTMLInputElement).focus()
      },


    },
    components: {Item},
    watch: {
        input(input) {
            if(input.length == 0) {
                this.resetInput()
            }
            this.$emit('update:input', this.input)
        }
    }
})
</script>


<template>
    <div class="search w-full overflow-visible">
        <form ref="form" class="w-full relative" :class="{searchPage: 'border-b'}" v-on:submit.prevent="submit">
            <q-input autocompletion="off" ref="input" :autofocus="autofocus" v-on:focus="onFocus" class="text-lg" :dense="dense" placeholder="Search Socialite" :style="{transform: `scale(${size})`}" v-debounce:1ms="search" :dark="$store.state.dark" rounded outlined v-model="input">
                <!-- <template #label>
                    Search
                </template> -->
                <template #prepend>
                    <q-icon size="30px" name="search" />
                </template>
                <template #append>
                    <q-icon class="close" size="30px" v-if="input.length > 0 && !loading" name="close" @click.stop="resetInput" />
                    <q-spinner-tail v-if="loading" size="30px" color="blue-grey" />
                </template>
            </q-input>
        </form>
        <div v-if="hasResults">
            <q-menu :autoClose="false" :no-focus="true" v-if="(!searchPage || !(['search', 'explore'].includes($route.name?.toString() ||  '')))" id="results" v-model="hasResults"
            class="bg-theme rounded-sm border-brighter"
            fit
            >
                <div class="results" v-if="results.length > 0" v-for="u in results">
                    <Item @click="input = ''" clickable :to="{ name: 'user-profile', params: { username: u.username } }" >
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
                <div v-if="noResults && !searchPage" class="results">
                    <q-item class="">
                        <q-item-section>
                            <q-item-label>No results found</q-item-label>
                        </q-item-section>
                    </q-item>
                </div> 
            </q-menu>
        </div>
    </div>
</template>

<style scoped lang="scss">


</style>