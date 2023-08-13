import http from "../../composables/http";
import { backend_baseURL } from "../../composables/backendURL";

export default defineEventHandler(async (event) => {
    // const res = await http.get(`${backend_baseURL}/users/user_from_cookie/`, {withCredentials: true})
    // const res = await $fetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'}).catch((error) => error.data)
    // console.log(res)
    return {
      hello: 'world'
    }
})