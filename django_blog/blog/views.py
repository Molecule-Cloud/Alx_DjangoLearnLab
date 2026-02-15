from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm


# Create your views here.
def home(request):
    return render(request, 'blog/base.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'blog/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.name}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user # Get the curret user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        user.save()

        messages.success(request, 'Profile updated')
        return redirect('profile')
    return render(request, 'blog/profle.html', {'user': request.user})



# === List View === #

# ===== LIST VIEW =====
class PostListView(ListView):
    """
    Display all blog posts
    URL: /posts/
    Template: blog/post_list.html
    Context variable: object_list (or post_list)
    """
    
    model = Post  # Which model to use
    template_name = 'blog/post_list.html'  # Custom template name
    context_object_name = 'posts' 
    ordering = ['-published_date']  # Newest first



class PostDetailView(DetailView):
    """
    Display a single blog post
    URL: /posts/1/
    Template: blog/post_detail.html
    Context variable: object (or post)
    """
    
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'



# blog/views.py - ADD THIS

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post
    URL: /posts/new/
    Template: blog/post_form.html
    Only accessible to logged-in users
    
    LoginRequiredMixin: Redirects to login if not authenticated
    """
    
    model = Post
    form_class = PostForm  # Use our custom form
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect after success
    
    def form_valid(self, form):
        """
        This runs when form is valid
        We set the author before saving
        """
        form.instance.author = self.request.user  # Set author = current user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing blog post
    URL: /posts/1/edit/
    Template: blog/post_form.html (reuses same form!)
    Only accessible to the post author
    
    UserPassesTestMixin: Allows custom permission check
    """
    
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """
        Permission test - runs automatically
        Returns True if user can access, False if not
        """
        post = self.get_object()  # Get the post being edited
        return self.request.user == post.author  # Only author can edit
    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post
    URL: /posts/1/delete/
    Template: blog/post_confirm_delete.html
    Only accessible to the post author
    """
    
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """Only author can delete"""
        post = self.get_object()
        return self.request.user == post.author