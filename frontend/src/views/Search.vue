<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { useStore } from '../store/store';
import { TouchSwipe } from 'quasar';
import Item from '../components/Item.vue';

export default defineComponent({
    data() {
        return {
            results: new Array<User>(),
            users: new Array<User>(),
            input: ref(''),
            loading: false,
            noResults: false,
            q: this.$route.query.q,
        };
    },
    name: 'search',
    setup() {
        const store = useStore()
    },
    created() {
        console.log(this.q)
        // window.scroll({
        //     top: 0,
        //     left: 0,
        //     behavior: 'smooth'
        // })
    },
    mounted() {
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
        // this.users = users.data.users
      },
      resetInput() {
        this.input = ""
        this.results = new Array<User>()
        this.noResults = false
      },
      submit() {

      }
    },
    components: {Item},
})
</script>


<template>
    <div class="search">
        <form v-on:submit.prevent="">
            <q-input
                v-model="input"
                dense
                :dark="$store.state.dark"
                :autofocus="true"
                placeholder="Search by username"
                v-debounce:1ms="search"
            >
                <template v-slot:prepend>
                    <q-icon @click="$router.go(-1)" class="back" name="arrow_back" />
                </template>
                <template v-slot:append>
                    <q-icon size="30px" v-if="input.length == 0" name="search" />
                    <q-icon class="close" size="30px" v-else-if="input.length > 0 && !loading" name="close" @click="resetInput" />
                    <q-spinner-tail v-else size="30px" color="blue-grey" />
                </template>
            </q-input>
        </form>
        <div id="results">
            <div class="results" v-if="results.length > 0" v-for="u in results">
                <!-- <q-item class="" clickable :to="{name: 'user-profile', params: {username: u.username}}">
                    <q-item-section avatar>
                        <img class="avatar" v-if="u.avatar" :src="u.avatar"/>
                        <q-icon size="50px" v-else name="account_circle" class="avatar__icon" />
                    </q-item-section>

                    <q-item-section>
                        <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label>
                        <q-item-label>{{ u.first_name }} {{ u.last_name }}</q-item-label>
                        <q-item-label caption>@{{ u.username }}</q-item-label>
                    </q-item-section>
                </q-item> -->
                <Item clickable :to="{ name: 'user-profile', params: { username: u.username } }" >
                    <template #avatar>
                        <img src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                        <!-- <img v-if="u.avatar" :src="u.avatar" alt="John Doe" class="rounded-full" /> -->
                        <!-- <q-icon size="50px" v-else name="account_circle" class="rounded-full" /> -->
                    </template>
                    <template #title>{{u.first_name + ' ' + u.last_name}}</template>
                    <template #caption>@{{ u.username }}</template>
                </Item>
            </div>
            <div v-if="noResults">
                <q-item class="">
                    <q-item-section>
                        <q-item-label>No results found</q-item-label>
                    </q-item-section>
                </q-item>
            </div> 
        </div>
        
    </div>
</template>

<style scoped>
* {
    color: var(--color-heading) !important;
}
.search {
    padding: 20px;
    width: 100%;
    height: 100vh;
    /* position: -webkit-sticky;
	position: sticky; */
    top: 0;
    
}

.back {
    cursor: pointer;
}

#results {
    max-height: 350px; 
    overflow: auto;  
}

.search-box{
  width: fit-content;
  height: fit-content;
  position: relative;
}
.input-search{
  height: 50px;
  width: 50px;
  border-style: none;
  padding: 10px;
  font-size: 18px;
  letter-spacing: 2px;
  outline: none;
  border-radius: 25px;
  transition: all .5s ease-in-out;
  background-color: var(--color-background);
  padding-right: 40px;
  color:white;
}
::placeholder{
  color: var(--color-text);
  font-size: 15px;
  font-weight: 500;
}
.btn-search{
  width: 50px;
  height: 50px;
  border-style: none;
  font-size: 20px;
  font-weight: bold;
  outline: none;
  cursor: pointer;
  border-radius: 50%;
  position: absolute;
  right: 0px;
  color: black;
  background-color:transparent;
  pointer-events: painted;  
}
.input-search{
  width: 300px;
  border-radius: 0px;
  background-color: transparent;
  border-bottom:1px solid var(--color-heading);
}
.input-search:focus{
  width: 300px;
  border-radius: 0px;
  background-color: transparent;
  border-bottom: 2px solid var(--color-heading);
  transition: all 1s cubic-bezier(0, 0.110, 0.35, 2);
}

.search-container{
    background: var(--color-background);
    height: 30px;
    border-radius: 30px;
    padding: 10px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: 0.8s;
    /*box-shadow:inset 2px 2px 2px 0px rgba(255,255,255,.5),
    inset -7px -7px 10px 0px rgba(0,0,0,.1),
   7px 7px 20px 0px rgba(0,0,0,.1),
   4px 4px 5px 0px rgba(0,0,0,.1);
   text-shadow:  0px 0px 6px rgba(255,255,255,.3),
              -4px -4px 6px rgba(116, 125, 136, .2);
  text-shadow: 2px 2px 3px rgba(255,255,255,0.5);*/
  box-shadow:  4px 4px 6px 0 rgba(255,255,255,.3),
              -4px -4px 6px 0 rgba(116, 125, 136, .2), 
    inset -4px -4px 6px 0 rgba(255,255,255,.2),
    inset 4px 4px 6px 0 rgba(0, 0, 0, .2);
}

.search-container:hover > .search-input{
    width: 200px;
}

.search-container .search-input{
    background: transparent;
    border: none;
    outline:none;
    width: 0px;
    font-weight: 500;
    font-size: 16px;
    transition: 0.8s;

}

.search-container .search-btn .fas{
    color: var(--color-text) !important;
    font-size: 30px;
    padding: 0px;
}

@keyframes hoverShake {
  0% {transform: skew(0deg,0deg);}
  25% {transform: skew(5deg, 5deg);}
  75% {transform: skew(-5deg, -5deg);}
  100% {transform: skew(0deg,0deg);}
}

.search-container:hover{
  animation: hoverShake 0.15s linear 3;
}

#results {
    border: 1px solid var(--color-border);
}

.results:nth-child(even) {
    background-color: var(--color-background-mute);
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.close {
    cursor: pointer;
}
</style>