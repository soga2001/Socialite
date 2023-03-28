import { store } from '@/store/store';
import axios from 'axios';
import { Crypter } from './crypter';
import { useCookies } from 'vue3-cookies';

const {cookies} = useCookies();

export const http = axios.create({
  baseURL: `http://localhost:8000/`,
  withCredentials: true,
  headers: {
      'X-CSRFToken': cookies.get('csrftoken')
    // "Cookie": 'csrftoken=' + Crypter.decrypt(store.state.csrf)
  },
})
