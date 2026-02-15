from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView
)

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

     # ===== BLOG POSTS (CRUD) =====
    # List all posts
    path('posts/', PostListView.as_view(), name='post_list'),
    
    # View single post (detail)
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # Create new post
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    
    # Edit post
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    
    # Delete post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
