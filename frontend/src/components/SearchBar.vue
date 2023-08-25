<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
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
        if(this.input.length === 0) {
            this.resetInput()
            return
        }
        console.log('here')
        this.loading = true
        await http.get(`users/username/${this.input}`).then((res) => {
            if(res.data.success) {
                this.noResults = false
                this.results = res.data.users
                this.hasResults = true;
            }
            else {
                this.noResults = true
                this.results = new Array<User>()
            }
        }).catch((err) => {
        })
        this.loading = false
      },
      resetInput() {
        this.input = ""
        this.noResults = false
        this.hasResults = false
        this.results = new Array<User>()
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
      },


    },
    components: {Item},
    watch: {
        input(input) {
            this.$emit('update:input', this.input)
            if(input.length == 0) {
                this.resetInput()
            }
            else {
                this.search()
            }
        },
        results(results) {
            console.log(results)
        }
    }
})
</script>


<template>
    <div class="search w-full overflow-visible">
        <form ref="form" class="w-full relative" :class="{searchPage: 'border-b'}" v-on:submit.prevent="submit">
            <q-input autocompletion="off" ref="input" :autofocus="autofocus" v-on:focus="onFocus" class="text-lg" :dense="dense" placeholder="Search Socialite" :style="{transform: `scale(${size})`}" debounce="500" :dark="$store.state.dark" rounded outlined v-model="input">
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