<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { useStore } from '../../store/store';

export default defineComponent({
    data() {
        return {
            results: new Array<User>(),
            users: new Array<User>(),
            input: ref(''),
            loading: false,
            noResults: false,
        };
    },
    setup() {
        const store = useStore()
    },
    created() {
        console.log('potato')
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
        // bottom 2 line is for whenevver # is used, will come into play at a later date
        // const re = /\s*(?:#|\s)/;
        // console.log(this.input.split(re))
        this.loading = true
        if(this.input === "") {
            this.results = []
            this.loading = false
            this.noResults = false
            return
        }
        await http.get(`users/username/${this.input}`).then((res) => {
            if(res.data.success) {
                this.results = res.data.users
            }
        })
        this.loading = false
        if(this.results.length == 0) {
            this.noResults = true
        }
        else {
            this.noResults = false
        }
        // this.users = users.data.users
      },
      submit() {

      }
    }
})
</script>


<template>
    <div class="home__sides__main">
        <form v-on:submit.prevent="">
            <q-input
                v-model="input"
                :dark="$store.state.dark"
                
                placeholder="Search by username"
                v-debounce:1s="search"
            >
                <template v-slot:append>
                    <q-icon size="30px" v-if="!loading || input.length == 0" name="search" />
                    <q-spinner-tail v-else size="30px" color="blue-grey" />
                </template>
            </q-input>
        </form>
        <div id="results">
            <div class="results" v-if="results.length > 0" v-for="u in results">
                <q-item class="" clickable :to="{name: 'user-profile', params: {id: u.id}}">
                    <q-item-section avatar>
                        <img class="avatar" v-if="u.profile.avatar" :src="u.profile.avatar"/>
                        <q-icon size="50px" v-else name="account_circle" class="avatar__icon" />
                    </q-item-section>

                    <q-item-section>
                        <!-- <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label> -->
                        <q-item-label>Suyogya Poudel</q-item-label>
                        <q-item-label caption>@{{ u.username }}</q-item-label>
                    </q-item-section>

                    <!-- <q-item-section side >
                        <q-icon name="more_horiz"  />
                    </q-item-section> -->
                </q-item>
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
.home__sides__main {
    padding: 20px;
    width: 100%;
    height: 100%;
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
</style>