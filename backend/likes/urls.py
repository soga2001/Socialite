from django.urls import path, re_path
from likes import views

urlpatterns = [
    # re_path(r'^like_post/(?P<post_id>\d+)/$', views.Like_Post.as_view(), name='like_post'),
    path('like_post/', views.Like_Post.as_view(), name='like_post'),
    re_path(r'^check_liked/(?P<post_id>[0-9a-f-]+)/$', views.Check_Liked.as_view(), name="check_liked"),
    # re_path(r'^check_liked/(?P<post_id>\d+)/$', views.Check_Liked.as_view(), name='check_liked'),
    re_path(r'^view_liked/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<username>\w+)/$', views.get_liked_post, name='view_liked'),
    # path('get_liked/', views.UserLiked.as_view(), name='get_liked'),

]