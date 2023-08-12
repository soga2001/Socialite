<script>
// import usefetch
import { useFetch } from 'nuxt/app';
// import { type Post } from '../../assets/interfaces';

export default {
    // data() {
    //     return {
    //         posts: Object as () => Post,
    //     }
    // },
    // methods: {
    //     fetchData() {
    //         const data = useFetch('api/posts');
    //         console.log(data);
    //     }
    // },
    // mounted() {
    //     this.fetchData()
    // }
    async fetch() {
        this.planets = await fetch('https://localhost:8000/users/').then((res) => {
            return res.json()
        })
    },
    data() {
        return {
            planets: [],
        }
    }
}
</script>

<template>
    <ul>
        
    </ul>

    <pre>{{ $data }}</pre>
</template>