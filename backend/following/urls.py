from django.urls import path, re_path
from following import views

urlpatterns = [
    re_path(r'^get_followers/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<user_id>\d+)/$', views.get_followers, name='get_followers'),
    re_path(r'^get_following/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<user_id>\d+)/$', views.get_following, name='get_following'),
    re_path(r'^follow_user/(?P<user_id>\d+)/$', views.Follow_User.as_view(), name='follow'),
    re_path(r'^get_if_followed/(?P<user_id>\d+)/$', views.get_followed_by_id, name='get_if_followed'),
]