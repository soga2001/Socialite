import { http } from "./http";
import { useCookies } from "vue3-cookies";
import { store } from "@/store/store";
import { Crypter } from "./crypter";

const cookies = useCookies();

export function get_csrf_token() {
    http.get("users/csrf/").then((res) => {
        // console.log(res);
        store.commit("setCSRF", res.data.csrf)
        cookies.cookies.set("csrf", Crypter.encrypt(res.data.csrf))
    }).catch((err) => {
        console.log(err)
    })
}