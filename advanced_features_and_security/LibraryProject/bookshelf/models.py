from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models import CASCADE



# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ([{self.publication_year}])"
    
    class Meta:
        permissions = [
            ('can_view_book', 'Can view book details'),
            ('can_create_book', 'Can create new books'),
            ('can_edit_book', 'Can edit existing books'),
            ('can_delete_book', 'Can delete books'),
            ('can_publish_book', 'Can publish or unpublish books'),
        ]

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ('can_publish_article', 'Can publish or unpublish articles'),
            ('can_view_article', 'Can view articles'),
            ('can_edit_article', 'Can edit articles'),
            ('can_delete_article', 'Can delete articles'),
            ('can_create_article', 'Can create articles'),
        ]



# === CUSTOM USER MODEL === #

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        #Normalaize Email -> lower case domain part && Create User Object
        email  = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  
        
        return self.create_user(email, password, **extra_fields)



# === Custom User Model === #

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_librarian(self):
        return self.role == 'LIBRARIAN'
    
    def is_member(self):
        return self.role == 'MEMBER'


    username = None
    email = models.EmailField(unique=True, verbose_name='email address')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date_of_Birth')
    profile_photo = models.ImageField(
        upload_to='profile_photos/', null=True, blank=True,
        verbose_name='Profile_Photo'
    )

    # == Use Custom User Manager === #
    objects = CustomUserManager()

    # === Set Email as USERNAME_FIELD  isnstead of USERNAME=== #
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'