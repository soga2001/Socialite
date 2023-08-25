from django.urls import path, re_path
from bugsreport import views

urlpatterns = [
    path('report_bugs/', views.Bugs.as_view(), name='post_content'),
    path('report_bugs/admin_access/', views.BugAdminAccess.as_view(), name='admin_access'),
]
