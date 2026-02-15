from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView
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

    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    path('posts/', PostListView.as_view(), name='post_list'),

    
    # Create: /post/5/comment/new/
    path('post/<int:post_id>/comment/new/', 
         CommentCreateView.as_view(), 
         name='comment_create'),
    
    # Edit: /post/5/comment/3/edit/
    path('post/<int:post_id>/comment/<int:pk>/edit/', 
         CommentUpdateView.as_view(), 
         name='comment_edit'),
    
    # Delete: /post/5/comment/3/delete/
    path('post/<int:post_id>/comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment_delete'),
]
