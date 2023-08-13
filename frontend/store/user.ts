import type { User } from "assets/interfaces"

interface State {
    // userList: UserInfo[]
    user: User,
    authenticated: boolean,
}
  
export const useUserStore = defineStore({
    id: 'user',
    state: (): State => ({
        user: {} as User,
        authenticated: false,

        
    }),
    actions: {
        async initStore() {
            this.user = {} as User
            this.authenticated = false  
            
            await http.get(`${backend_baseURL}/users/user_from_cookie/`).then((res) => {
                if(res.data.success) {
                    this.setUser(res.data.user)
                    this.setAuthenticated(true)
                }
            }).catch((err) => {
                this.setUser({} as User)
                this.setAuthenticated(false)
            })
        },
        setUser(user: User) {
            this.user = user
        },
        setAuthenticated(authenticated: boolean) {
            this.authenticated = authenticated
        },
        logout() {
            http.get(`${backend_baseURL}/users/logout/`).then((res) => {
                if(res.data.success) {
                    this.user = {} as User
                    this.authenticated = false
                }
            }).catch((err) => {})
        }
    }
})
  

// export const userStore = useUserStore()