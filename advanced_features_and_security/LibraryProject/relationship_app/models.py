from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver




# == User Profile Model === #

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    ]

    user = models.OneToOneField(
        User, on_delete = models.CASCADE, related_name='profile'
    )

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES,
    default='MEMBER'
    )



    def __str__(self):
        return f"{self.user.username} - {self.role}"
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_librarian(self):
        return self.role == 'LIBRARIAN'
    
    def is_member(self):
        return self.role == 'MEMBER'

    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# === Library Models === #
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_add_book', 'Can add new books to the system'),
            ('can_change_book', 'can edit existing book details'),
            ('can_delete_book', 'can remove books from database')
        ]

    

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book, related_name='libraries'
    )
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library, on_delete=models.CASCADE,
        related_name='librarian'
    )

    def __str__(self):
        return f"{self.name} - {self.library.name}"




