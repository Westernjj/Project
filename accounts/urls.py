# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',  auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('resend/', views.resend, name='resend'),
    # Шлях для ПЕРЕГЛЯДУ профілю
    path('profile/', views.profile, name='profile'),
    # Новий шлях для РЕДАГУВАННЯ профілю
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]