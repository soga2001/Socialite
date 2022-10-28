<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { useStore } from '../../store/store';

export default defineComponent({
    data() {
        return {
            users: new Array<User>(),
            input: ref('')
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
        http.get(`users/username/${this.input}`).then((res) => {
            if(res.data.success) {
                this.users = res.data.users
                console.log(this.users)
            }
        })
        // this.users = users.data.users
      }
    }
})
</script>


<template>
    <div class="home__sides__main">
        <form v-on:submit.prevent="">
            <!-- <div class="search-box">
                <button class="btn-search" ><q-icon name="search"/></button>
                <input type="text" class="input-search" placeholder="Search by username">
            </div> -->
            <!-- <div class="search-container">
                <input type="text" name="search" placeholder="Search..." class="search-input">
                <a href="#" class="search-btn">
                    <q-icon name="search" class="fas fa-search"/>     
                </a>
            </div> -->
            <q-input
                v-model="input"
                :dark="$store.state.dark"
                filled
                placeholder="Search by username"
                v-debounce:1s="search"
            >
                <template v-slot:append>
                <q-icon name="search" />
                </template>
            </q-input>
        </form>
    </div>
</template>

<style scoped>
* {
    color: var(--color-heading) !important;
}
.home__sides__main {
    display: flex;
    justify-content: center;
    padding: 20px;
    width: 100%;
    height: 10vh;
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
.input-search::placeholder{
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

.results {
    background-color: var(--color-background-soft);
}

</style>