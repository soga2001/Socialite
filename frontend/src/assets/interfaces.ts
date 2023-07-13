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
    user_permissions: string[],
    avatar: '',
    banner: '',
    bio: '',
    total_posted: number,
    total_followers: number,
    total_following: number,
    date_joined: string,
}


export interface Post{
    user_id: any
    id: string,
    username: string,
    user_avatar: string,
    user: number,
    img_url: string,
    caption: string,
    date_posted: string,
    date_updated: string,
    total_likes: number,
    total_comments: number,
}

export interface Comment{
    id: number,
    username: string,
    user_avatar: string,
    post: string,
    comment: string,
    date_posted: string,
    date_updated: string,
}

export interface Notifications {
    id: number;
    level: string;
    actor: string,
    actor_avatar: string,
    unread: boolean;
    actor_object_id: string;
    verb: string;
    description: string;
    target_object_id: string;
    action_object_object_id: string;
    timestamp: string;
    public: boolean;
    deleted: boolean;
    emailed: boolean;
    data: string;
    link: string;
    recipient: number;
    actor_content_type: number;
    target_content_type: string;
    action_object_content_type: string;
}