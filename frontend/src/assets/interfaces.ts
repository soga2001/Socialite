export interface User{
    id: number,
    username: string,
    email?: string,
    first_name: string,
    last_name: string,
    full_name: string,
    last_login: string,
    private: boolean,
    verified: boolean,


    is_active: boolean,
    is_staff: boolean,
    is_admin: boolean,
    is_current_user: boolean,
    is_superuser: boolean,
    is_following?: boolean,

    groups: string[],
    user_permissions: string[],

    avatar: '',
    banner: '',
    bio: '',

    total_posted: number,
    total_followers: number,
    total_following: number,
    date_joined: string,
    notification_on: boolean,

    location: string,
    link: string,
    dob: string,
    phone: string,
}


export interface Post{
    id: string,
    img_url: string,
    caption: string,
    date_posted: string,
    date_updated: string,
    total_likes: number,
    total_comments: number,
    user: User,
    user_has_liked: boolean,
    is_owner: boolean,
    all_liked_users: User[],
}

export interface LikesDetail {
    id: number,
    user: User,
}

export interface Comment{
    id: number,
    user: User,
    username: string,
    user_avatar: string,
    post: string,
    comment: string,
    date_posted: string,
    date_updated: string,
    is_owner: boolean,
}

export interface NotificationDataAsset {
    url: string,
    text: string,
}

export interface Notifications {
    id: number;
    level?: string;
    actor: User,
    unread: boolean;
    actor_object_id?: string;
    verb: string;
    description: string;
    target_object_id?: string;
    action_object_object_id?: string;
    timestamp: string;
    public: boolean;
    deleted: boolean;
    emailed: boolean;
    recipient: number;
    actor_content_type: number;
    target_content_type?: string;
    action_object_content_type?: string;
    created: string;
    data?: NotificationDataAsset;
}

export interface Following {
    followed_date: string,
    followed_user: User,
    following_user: string,
    id: string,
    notification: boolean,
}

export interface Follower {
    followed_date: string,
    followed_user: string,
    following_user: User,
    id: string,
    notification: boolean,
}

export interface Sessions {
    session_key: string,
    current_session: boolean,
    expire_date: string,
    user_agent: string,
    last_activity: string,
    ip: string,
    user: string,
}