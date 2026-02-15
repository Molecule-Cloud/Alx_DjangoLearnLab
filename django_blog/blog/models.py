from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# == User Model == #
# class User(User):
#     email = models.EmailField(unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     def __str__(self):
#         return self.email


# == Post Model == #
class Post(models.Model):
    """
    Blog Post Model for a single blog entry with each row representing a row in the database table
    """
    title = models.CharField(max_length = 200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
    
    class Meta:
        # Add newest posts first
        ordering = ['-published_date']



class Comment(models.Model):
    """
    Comment model for blog posts
    
    Each comment is tied to:
    - One specific post (ForeignKey)
    - One user who wrote it (ForeignKey)
    """
    
    # Which post this comment belongs to
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,  # If post deleted, delete its comments
        related_name='comments'     # Allows post.comments.all()
    )
    
    # Who wrote this comment
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # If user deleted, delete their comments
        related_name='comments'      # Allows user.comments.all()
    )
    
    # The comment text
    content = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Set when created
    updated_at = models.DateTimeField(auto_now=True)      # Updates on every save
    
    class Meta:
        ordering = ['-created_at']  # Show newest comments first
    
    def __str__(self):
        """String representation"""
        return f'Comment by {self.author.username} on {self.post.title}'