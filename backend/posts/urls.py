from django.urls import path, re_path
from posts import views

urlpatterns = [
    path('post_content/', views.Post_Content.as_view(), name='post_content'),
    path('delete_post/', views.Post_Content.as_view(), name="delete_post"),
    # re_path(r'^delete_post/(?P<post_id>\d+)/$', views.Delete_Post.as_view(), name="delete_post"),
    re_path(r'^view_posts/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/$', views.view_posts, name='view_posts'),
    re_path(r'^user_posted/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<user_id>\d+)/$', views.user_posted, name='view_posts'),
    re_path(r'^user_posted_total/(?P<user_id>\d+)/$', views.total_user_posted, name='total_user_posted'),
    re_path(r'^view_post_by_id/(?P<post_id>\d+)/$', views.view_post_by_id, name='view_post_by_id'),
    path('delete_all_posts/', views.delete_all_posts, name="delete_all_posts"),
    # re_path(r'^delete_post/(?P<post_id>\d+)/$', views.Delete_Post.as_view(), name="delete_post"),
]