// import http 
import http from '../../composables/http';
import type { Post } from '../../assets/interfaces';
import { backend_baseURL } from '../../composables/backendURL';

export default defineEventHandler(async (event) => {
  // const res = await $fetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'}).catch((error) => error.data)
  // console.log(res)
  return {
    hello: 'world'
  }
})