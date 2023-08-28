import axios from 'axios';
import { Notify } from 'quasar'
import { store } from '@/store/store';
import router from '@/router';

export const http = axios.create({
  baseURL: `https://localhost:8000/`,
  withCredentials: true,
})

http.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if(error.response.status === 401 && store.state.authenticated) {
      Notify.create({
        message: `<span class="text-white weight-900">Your account may not be allowed to perform this action. Please refresh the page and try again.</span>`,
        position: 'bottom',
        timeout: 2000,
        classes: 'bg-web-theme',
        html: true,
        actions: [
          { label: 'Refresh', color: 'white', handler: () => {window.location.reload()} }
        ]
      })
    }
    return Promise.reject(error);
  }
);
