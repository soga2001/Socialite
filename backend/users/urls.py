from django.urls import path, re_path
from users import views
from . import consumers

urlpatterns = [
    path('', views.users, name="users"),
    path('csrf/', views.get_csrf, name="csrf"),
    re_path(r'^user/(?P<user_id>\d+)/$', views.user_by_id, name="user_by_id"),
    re_path(r'^username/(?P<username>[\w\s]+)?/$', views.user_by_username, name="user_by_username"),
    re_path(r'^username/(?P<username>[\w\s]+)/(?P<multiple>\w+)?/$', views.user_by_username, name="user_by_username"),
    path('user_sessions/', views.AllSessions.as_view(), name="all sessions"),
    path('delete_session/', views.DeleteSpecificSession.as_view(), name="session detail"),
    path('user_from_cookie/', views.UserFromCookie.as_view(), name="user from cookie"),
    path('flush_session/', views.flush_session, name="flush session"),
    # path('get_session', views.get_session, name="get session"),
    # path('delete_session/', views.get_session_key, name="get session key"),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('delete_all/', views.delete_all, name="delete"),
    path('make_staff/', views.Staff.as_view(), name="make_staff"),
    path('update_profile/', views.UpdateProfile.as_view(), name="make_superuser"),
    path('verify_email/', views.verify_email, name="verify_email"),
    path('send_reset_password_email/', views.email_forgot_password_link, name="forgot password link"),
    path('reset_password/', views.reset_password, name="reset password"),
    path('change_password/', views.ChangePassword.as_view(), name="change password"),
    path('get_user_info/', views.UserInfo.as_view(), name="get user information"),
    path('delete_account/', views.DeleteAccount.as_view(), name="delete account"),
    path('verify_user/', views.VerifyUser.as_view(), name="verify user"),
    path('make_staff/', views.Staff.as_view() , name="verify user"),
    # re_path(r'^verify_user/(?P<user_id>\d+)/$', views.VerifyUser.as_view(), name="verify user")
]
