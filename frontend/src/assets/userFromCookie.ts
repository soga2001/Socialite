import { http } from "./http";
import { useCookies } from "vue3-cookies";
import { store } from "@/store/store";

const cookies = useCookies();

export async function get_user_from_cookie() {
    await http.get("users/user_from_cookie/").then( async (res) => {
        // console.log(res);
        if(res.data.success) {
            await store.commit("setUser", res.data.user)
            await store.commit('authenticate', true)
            console.log(store.state.authenticated)
        }
        
    }).catch((err) => {
        
    })
    return true
}