from django.urls import path
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('delete_user/', views.Delete.as_view(), name="delete_user"),
    path('delete_all/', views.delete_all, name="delete")
]