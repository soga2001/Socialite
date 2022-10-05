from django.urls import path, re_path
from userprofile import views

urlpatterns = [
    path('update_profile/', views.update_profile , name='update_profile'),
    path('get_profile/', views.get_profile , name='get_profile'),
]