from webbrowser import get

from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from rest_framework import generics, permissions, status
from .serializers import PostSerializer, CommentSerializer, PostCreateUpdateSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom Persmission to allow only authors to edit or delete their posts and comments."""

    def has_object_permission(self, request, view, obj):
        # Allow read permissions to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.Method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostListCreateView(generics.ListCreateAPIView):
    """
    View to list all posts and create new posts 
    """ 

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    """
     Override the get_serializer_class method to return different serializers based on the request method.
    """
    def get_serializer(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve, update or delete a specific post.
    GET: Retrieve a post by its ID.
    PUT/PATCH: Update a post by its ID (only the author can update).
    DELETE: Delete a post by its ID (only the author can delete).
    """
    queryset= Post.objects.all().order_by('-created_at')
    serializer_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostSerializer
    



class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to list all comments for a specific post and create new comment for a specific posts.
    GET: List all comments for a specific post.
    POST: Add a comment to a post (only authenticated users can comment).
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def queryset(self):
        """
        Filter comments to only those related to the specified post, ordered by creation time (newest first).
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)



class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a specific comment.
    GET: Retrieve a comment by its ID.
    PUT/PATCH: Update a comment by its ID (only the author can update).
    DELETE: Delete a comment by its ID (only the author can delete).
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    