from django.urls import path, re_path
from userprofile import views

urlpatterns = [
    path('update_profile/', views.Update_Profile.as_view() , name='update_profile'),
    # path('get_profile/', views.get_profile , name='get_profile'),
    re_path(r'^get_profile/(?P<user_id>\d+)/$', views.get_profile, name="get_profile"),
]