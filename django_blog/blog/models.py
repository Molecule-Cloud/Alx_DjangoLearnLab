from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.utils.text import slugify  # Add this import at the top

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
    tags = models.ManyToManyField(
        Tag,
        related_name='posts',      # Allows tag.posts.all()
        blank=True  
    ) 

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
    


class Tag(models.Model):
    """
    Tag model for categorizing posts
    
    Tags are like labels that can be applied to multiple posts
    Each tag has a unique name and automatically generated slug for URLs
    """
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        """
        Automatically create slug from name
        Example: "Django Tips" → "django-tips"
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """URL for tag detail page"""
        from django.urls import reverse
        return reverse('tag_detail', args=[self.slug])