import axios from 'axios';

export const http = axios.create({
  baseURL: `https://localhost:8000/`,
  withCredentials: true,
})

