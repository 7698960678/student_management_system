from django.urls import path
from .views import *

urlpatterns = [
    path('login',LoginView.as_view(),name='Login-View'),
    path('admin-signup',AdminSignupView.as_view(),name='Admin-Signup-View'),
    path('teacher-signup',TeacherSignupView.as_view(),name='Teacher-Signup-View'),
    path('student-signup',StudentSignupView.as_view(),name='Student-Signup-View'),
]