from django.urls import path, re_path
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    re_path(r'^user/(?P<user_id>\d+)/$', views.user_by_id, name="user_by_id"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('delete_user/', views.Delete.as_view(), name="delete_user"),
    path('delete_all/', views.delete_all, name="delete")
]
