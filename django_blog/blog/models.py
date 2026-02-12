from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# == User Model == #
class User(User):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


# == Post Model == #
class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField(max_length=100)
    published_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)