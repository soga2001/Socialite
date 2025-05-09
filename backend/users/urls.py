from django.urls import path, re_path
from users import views

urlpatterns = [
    path('', views.AllUsers.as_view(), name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    re_path(r'^user/(?P<user_id>[0-9a-f-]+)/$', views.user_by_id, name="user_by_id"),

    re_path(r'^username/(?P<username>[\w\s]+)/$', views.user_by_username, name="user_by_username"),
    re_path(r'^username/(?P<username>[\w\s]+)/multiple/$', views.user_by_username, name="user_by_username_multiple"),

    path('user_sessions/', views.AllSessions.as_view(), name="all_sessions"),
    path('session/', views.SpecificSession.as_view(), name="session_detail"),
    path('user_from_cookie/', views.UserFromCookie.as_view(), name="user_from_cookie"),
    path('flush_session/', views.flush_session, name="flush_session"),

    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('delete_all/', views.delete_all, name="delete_all"),
    path('make_staff/', views.Staff.as_view(), name="make_staff"),
    path('update_profile/', views.UpdateProfile.as_view(), name="update_profile"),

    path('verify_email/', views.verify_email, name="verify_email"),
    path('send_reset_password_email/', views.email_forgot_password_link, name="send_reset_password_email"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('change_password/', views.ChangePassword.as_view(), name="change_password"),
    path('get_user_info/', views.UserInfo.as_view(), name="get_user_info"),
    path('delete_account/', views.DeleteAccount.as_view(), name="delete_account"),
    path('verify_user/', views.VerifyUser.as_view(), name="verify_user"),
]
