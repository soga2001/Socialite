from django.urls import path, re_path
from notification import views

urlpatterns = [
    path('all/', views.NotificationView.as_view(), name='post_content'),
    path('mentions/', views.Mentions.as_view(), name='mentions'),
    path('mark_all_as_read/', views.MarkAllAsRead.as_view(), name='mark_all_as_read'),
    path('mark_as_read/', views.MarkAsRead.as_view(), name='mark_as_read'),
]
