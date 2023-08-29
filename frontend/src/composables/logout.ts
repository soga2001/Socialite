import { http } from "@/assets/http";
import { store } from "@/store/store";
import router from '@/router/index';
import { Notify } from 'quasar'

export const logout = async () => {
    await http.post("users/logout/").then((res) => {
        Notify.create({
            message: `<span class="text-white weight-900">Logout successful</span>`,
            position: 'top-right',
            timeout: 2000,
            classes: 'bg-web-theme',
            html: true,
        })
        store.commit("authenticate", false);
        store.commit("setDefaultUser");
    }).catch((err) => {
    });
}