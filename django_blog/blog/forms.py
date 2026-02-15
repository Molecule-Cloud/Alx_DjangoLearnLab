from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment
from .models import Post, Comment, Tag


class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ['usrname', 'email', 'password1', 'password2']

    def __inti__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        
        return email



class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    Now includes tag selection
    """
    
    # Add a field for tags
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 5  # Show 5 tags at a time
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Add 'tags' to fields
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
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to every field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })



class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments
    
    Only includes 'content' field because:
    - post is set automatically from URL
    - author is set automatically from logged-in user
    """
    
    class Meta:
        model = Comment
        fields = ['content']  # Only show the content field
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
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