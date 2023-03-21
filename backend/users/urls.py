from django.urls import path, re_path
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    re_path(r'^user/(?P<user_id>\d+)/$', views.user_by_id, name="user_by_id"),
    re_path(r'^username/(?P<username>\w+)?/$', views.user_by_username, name="user_by_username"),
    re_path(r'^username/(?P<username>\w+)/(?P<multiple>\w+)?/$', views.user_by_username, name="user_by_username"),
    path('all_logins/', views.AllLogins.as_view(), name="all sessions"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('delete_user/', views.Delete_User.as_view(), name="delete_user"),
    path('delete_all/', views.delete_all, name="delete"),
    path('make_staff/', views.Staff.as_view(), name="make_staff"),
]
