# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

class TagWidget(forms.TextInput):
    """
    Custom widget for tag input
    Allows users to enter tags as comma-separated values
    """
    def __init__(self, attrs=None):
        default_attrs = {
            'placeholder': 'Enter tags separated by commas (e.g., python, django, web)',
            'class': 'form-control tag-input'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """Format the value for display in the input field"""
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        # If value is a queryset or list of tags, convert to comma-separated string
        try:
            return ', '.join(tag.name for tag in value.all())
        except (AttributeError, TypeError):
            return str(value)


class UserRegisterForm(UserCreationForm):
    """Custom registration form with email field"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
    
    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    Now includes tag handling with custom TagWidget
    """
    
    # Custom tag field using TagWidget
    tags_input = forms.CharField(
        required=False,
        widget=TagWidget()
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form and pre-fill tags input if editing"""
        super().__init__(*args, **kwargs)
        
        # Add 'form-control' class to every field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
        
        # If this is an existing post (has instance), pre-fill tags_input
        if self.instance and self.instance.pk:
            # Get existing tags as comma-separated string
            existing_tags = ', '.join(tag.name for tag in self.instance.tags.all())
            self.initial['tags_input'] = existing_tags
    
    def clean_tags_input(self):
        """
        Validate and parse tag input
        Converts comma-separated string into list of tag names
        """
        tags_string = self.cleaned_data.get('tags_input', '')
        if not tags_string:
            return []
        
        # Split by comma and clean up whitespace
        tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        
        # Optional: Validate tag names (no special characters, reasonable length)
        for tag_name in tag_names:
            if len(tag_name) > 50:
                raise forms.ValidationError(
                    f'Tag "{tag_name}" is too long (max 50 characters)'
                )
        
        return tag_names
    
    def save(self, commit=True):
        """
        Save the post and handle tag creation/association
        """
        # Save the post first
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Handle tags
            tag_names = self.cleaned_data.get('tags_input', [])
            
            # Clear existing tags
            post.tags.clear()
            
            # Create or get tags and add to post
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': tag_name.lower().replace(' ', '-')}
                )
                post.tags.add(tag)
        
        return post


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control comment-input',
                'placeholder': 'Write your comment here...',
                'rows': 3,
                'maxlength': 1000
            }),
        }
        labels = {
            'content': ''  # Remove label
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional CSS classes
        self.fields['content'].widget.attrs.update({
            'class': 'form-control comment-input'
        })