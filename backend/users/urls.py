from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('delete_all/', views.delete_all, name="delete")
]