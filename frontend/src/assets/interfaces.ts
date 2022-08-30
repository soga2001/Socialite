export interface User{

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