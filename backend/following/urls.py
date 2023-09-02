from django.urls import path, re_path
from following import views

urlpatterns = [
    # re_path(r'^get_followers/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<user_id>\d+)/$', views.get_followers, name='get_followers'),
    # re_path(r'^get_following/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/$', views.get_following, name='get_following'),
    re_path(r'^follow_user/(?P<user_id>[0-9a-f-]+)/$', views.Follow_User.as_view(), name='follow'),
    re_path(r'^get_if_followed/(?P<user_id>[0-9a-f-]+)/$', views.get_followed_by_id, name='get_if_followed'),
    re_path(r'^get_following_users/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<username>[\w\s]+)?/$', views.GetFollowing.as_view(), name="get following"),
    re_path(r'^get_followers_users/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<username>[\w\s]+)?/$', views.GetFollowers.as_view(), name="get followers"),
]