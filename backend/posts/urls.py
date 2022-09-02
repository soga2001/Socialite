from django.urls import path
from posts import views

urlpatterns = [
    path('post_content/', views.Post_Content.as_view(), name='post_content'),
    path('view_posts/', views.view_posts, name='view_posts'),
    path('delete_all_posts/', views.delete_posts, name="delete_posts")
]