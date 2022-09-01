export interface User{
    id: number,
    username: string,
    email: string,
    first_name: string,
    last_name: string,
    is_active: boolean,
    is_staff: boolean,
    is_superuser: boolean,
    last_login: string,
    groups: string[],
    user_permissions: string[]
}

export interface Post{
    id: number,
    username: string,
    user_id: number,
    img_url: string,
    caption: string,
    date_posted: string,
    date_updated: string
}