from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.attendance.views import AcademicClassViews,AttendanceViews,TakeAttendanceViews,LoginView,\
    DashboardViews,logout_view,DashboardAPIView
urlpatterns = [
    path('', AcademicClassViews.as_view(),name="get-class-list"),
    path('get/<str:class_id>',AttendanceViews.as_view(),name="get-attendance"),
    path('take/<str:class_id>',TakeAttendanceViews.as_view(),name="take-attendance"),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/',DashboardViews.as_view(),name="dashboard"),
    path('logout/', logout_view, name='logout'),
    path('api/v1/dashboard/', DashboardAPIView.as_view(), name='student-list'),
]