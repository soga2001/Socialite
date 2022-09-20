from django.urls import path, re_path
from posts import views

urlpatterns = [
    path('post_content/', views.Post_Content.as_view(), name='post_content'),
    # re_path(r'^username/(?P<username>\w+)/$', views.user_by_username, name="user_by_username"),
    re_path(r'^view_posts/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/', views.view_posts, name='view_posts'),
    path('delete_all_posts/', views.delete_posts, name="delete_posts")
]