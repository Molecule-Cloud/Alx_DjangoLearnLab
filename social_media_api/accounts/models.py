from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model for Authentication

class CustomUser(AbstractUser):
    """
    Custom user model for the Social Media API project.
    """

    bio = models.TextField(max_length=500, blank = True, help_text ="Tell us a little about yourself")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    class Meta:
        ordering = ['-date_joined']