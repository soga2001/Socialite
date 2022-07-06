from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('delete_user/', views.Delete.as_view(), name="delete_user"),
    path('delete_all/', views.delete_all, name="delete")
]