from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment




class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment Model to handle serializations and deserialization of Comment data
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'author_id', 'content', 'created_at', 'updated_at']




class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post Model to handle serializations and deserialization of Post data
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ['id', 'post', 'author', 'author_username', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Post instances, excluding comments and comment count
    """
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content']

        def create(self, validated_data):
            return super().create(validated_data)