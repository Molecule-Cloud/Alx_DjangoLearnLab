from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:post_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]