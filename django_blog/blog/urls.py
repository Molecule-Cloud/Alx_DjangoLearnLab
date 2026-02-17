# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    # Post views
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView,
    
    # Comment views
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    
    # Tag and search views
    TagListView, TagDetailView, PostSearchView
)

urlpatterns = [
    # ===== HOME =====
    path('', views.home, name='home'),
    
    # ===== AUTHENTICATION =====
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # ===== BLOG POSTS (CRUD) =====
    # List all posts
    path('posts/', PostListView.as_view(), name='post_list'),
    
    # Create new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # View single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # Update post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    
    # Delete post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # ===== COMMENTS =====
    # Create comment on a post - MATCHES: post/<int:pk>/comments/new/
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    
    # Update comment - MATCHES: comment/<int:pk>/update/
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    
    # Delete comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    # ===== TAGGING =====
    # List all tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    
    # View posts by tag
    path('tag/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
    
    # ===== SEARCH =====
    # Search posts
    path('search/', PostSearchView.as_view(), name='post_search'),
]