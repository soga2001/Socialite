from django.urls import path
from posts import views

urlpatterns = [
    path('view_posts/', views.view_posts, name='view_posts'),
    path('post/', views.Post_Content.as_view(), name='post')
]