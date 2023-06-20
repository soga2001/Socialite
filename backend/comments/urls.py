from django.urls import path, re_path
from comments import views

from . import consumers 

urlpatterns = [
    re_path(r'^comment/$', views.Comments.as_view(), name='comments by user'),
    re_path(r'^comment/(?P<id>\d+)/$', views.Comments.as_view(), name='comments by user'),
    re_path(r'^comment/(?P<post_id>[0-9a-f-]+)/$', views.Comments.as_view(), name='comment_detail'),
    re_path(r'^comments_by_post/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<post_id>[0-9a-f-]+)/$', views.comments_by_post, name='comments_by_post'),
    # re_path(r'^comments_by_user/(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)/(?P<page>\w+)/(?P<user_id>\d+)/$', views.comments_by_user, name='comments_by_user'),
    # re_path(r'^total_comments_by_user/(?P<user_id>\d+)/$', views.total_comments_by_user, name='total_comments_by_user'),
    # re_path(r'^total_comments_by_post/(?P<post_id>\d+)/$', views.total_comments_by_post, name='total_comments_by_post'),
    # path('delete_all_comments/', views.delete_all_comments, name="delete_all_comments"),
]


websocket_urlpatterns = [
    re_path(r'^ws/spill_comments/(?P<post_id>[0-9a-f-]+)/$', consumers.SpillCommentConsumer.as_asgi()),
    re_path(r'^ws/comment/(?P<comment_id>\d+)/$', consumers.CommentConsumer.as_asgi()),
]