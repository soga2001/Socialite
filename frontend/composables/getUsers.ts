import type { UseFetchOptions } from 'nuxt/app'
import { defu } from 'defu'

export function useCustomFetch<T> (url: string, options: UseFetchOptions<T> = {}) {
  const userAuth = useCookie('token')
  const config = useRuntimeConfig()

  const defaults: UseFetchOptions<T> = {
    baseURL: config.baseUrl as string ?? 'http://localhost:8000',
    // cache request
    key: url,

    // // set user token if connected
    // headers: userAuth.value
    //   ? { Authorization: `Bearer ${userAuth.value}` }
    //   : {},

    // onResponse (_ctx) {
    //   // _ctx.response._data = new myBusinessResponse(_ctx.response._data)
    // },

    // onResponseError (_ctx) {
    //   // throw new myBusinessError()
    // }
  }
  const params = defu(options, defaults)

  return useFetch(url, params, )
}
