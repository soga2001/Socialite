from django.urls import path, re_path
from notification import views

urlpatterns = [
    path('all/', views.NotificationView.as_view(), name='post_content'),
    path('mentions/', views.Mentions.as_view(), name='mentions'),
]