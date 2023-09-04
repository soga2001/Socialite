import { http } from "./http";
import { store } from "@/store/store";


export async function get_user_from_cookie() {
    await http.get("users/user_from_cookie/").then( async (res) => {
        // console.log(res);
        if(res.data.success) {
            await store.commit("setUser", res.data.user)
            await store.commit("authenticate", true);
            await store.commit('setLoading', false)
        }
        
    }).catch(async (err) => {
        console.clear()
    })
    return true
}