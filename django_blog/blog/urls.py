from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # ===== AUTHENTICATION URLS =====
    
    path('register/', views.register, name='register'),
    
    # Login - Using Django's built-in view
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'  # Custom template
    ), name='login'),
    
    # Logout - Using Django's built-in view
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'  # Redirect to home after logout
    ), name='logout'),
    
    path('profile/', views.profile, name='profile'),
]