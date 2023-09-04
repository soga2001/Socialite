import { http } from "./http";
import { store } from "@/store/store";

export function get_csrf_token() {
    http.get("users/csrf/").then((res) => {
        // console.log(res);
        store.commit("setCSRF", res.data.csrf)
    }).catch((err) => {
        console.log(err)
    })
}