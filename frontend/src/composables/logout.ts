import { http } from "@/assets/http";
import { store } from "@/store/store";
import router from '@/router/index';

export const logout = async () => {
    await http.post("users/logout/").then((res) => {
        store.commit("authenticate", false);
        store.commit("setDefaultUser");
    }).catch((err) => {
        if (err.response.status === 401) {
            router.go(0)
        }
    });
}