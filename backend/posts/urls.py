from django.urls import path, re_path
from posts import views

urlpatterns = [
    path('post_content/', views.Post_Content.as_view(), name='post_content'),
    path('delete_post/', views.Post_Content.as_view(), name="delete_post"),
    path('post_by_id/<uuid:post_id>/', views.get_post_by_id, name="post_by_id"),
    # re_path(r'^post_by_id/(?P<post_id>[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$', views.get_post_by_id, name="post by id"),
    # re_path(r'^delete_post/(?P<post_id>\d+)/$', views.Delete_Post.as_view(), name="delete_post"),
    re_path(r'^posts_by_followed_users/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/$', views.post_by_followed_users, name='posts_by_followed_users'),
    re_path(r'^explore/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\d+)/$', views.explore, name="explore"),
    re_path(r'^view_posts/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/$', views.view_posts, name='view_posts'),
    # re_path(r'^user_posted/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<user_id>\d+)/$', views.user_posted, name='view_posts'),
    re_path(r'^user_posted/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<username>\w+)/$', views.user_posted, name='view_liked'),
    re_path(r'^user_posted_total/(?P<user_id>[0-9a-f-]+)/$', views.total_user_posted, name='total_user_posted'),
    path('delete_all_posts/', views.delete_all_posts, name="delete_all_posts"),
    # re_path(r'^delete_post/(?P<post_id>\d+)/$', views.Delete_Post.as_view(), name="delete_post"),
]