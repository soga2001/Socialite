import { store } from '@/store/store';
import axios from 'axios';
import { Crypter } from './crypter';

export const http = axios.create({
  baseURL: `http://localhost:8000/`,
//   xsrfCookieName: '',
  headers: {
    // "Cookie": 'csrftoken=' + Crypter.decrypt(store.state.csrf)
    'X-CSRFToken': Crypter.decrypt(store.state.csrf),
    
  },
})