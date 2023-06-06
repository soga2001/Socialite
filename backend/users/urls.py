from django.urls import path, re_path
from users import views

urlpatterns = [
    path('', views.users, name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    re_path(r'^user/(?P<user_id>\d+)/$', views.user_by_id, name="user_by_id"),
    re_path(r'^username/(?P<username>[\w\s]+)?/$', views.user_by_username, name="user_by_username"),
    re_path(r'^username/(?P<username>[\w\s]+)/(?P<multiple>\w+)?/$', views.user_by_username, name="user_by_username"),
    path('all_logins/', views.AllLogins.as_view(), name="all sessions"),
    # path('check_cookies/', views.check_cookie, name="check cookies"),
    path('user_from_cookie/', views.UserFromCookie.as_view(), name="user from cookie"),
    path('flush_session/', views.flush_session, name="flush session"),
    path('get_session', views.get_session, name="get session"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('delete_user/', views.Delete_User.as_view(), name="delete_user"),
    path('delete_all/', views.delete_all, name="delete"),
    path('make_staff/', views.Staff.as_view(), name="make_staff"),
    path('update_profile/', views.UpdateProfile.as_view(), name="make_superuser"),
    # path('upload_avatar/', views.UploadAvatar.as_view(), name="upload avatar"),
    # path('upload_banner/', views.UploadBanner.as_view(), name="upload banner"),
]
